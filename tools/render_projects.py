#!/usr/bin/env python3
"""Render the project cards inside index.html from projects.json."""
from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "projects.json"
INDEX = ROOT / "index.html"
START = "<!-- PROJECTS:START -->"
END = "<!-- PROJECTS:END -->"


def load_projects() -> list[dict]:
    if not MANIFEST.exists():
        return []
    with MANIFEST.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise SystemExit("projects.json must contain a JSON array")
    return [p for p in data if isinstance(p, dict) and p.get("slug")]


def sort_key(project: dict) -> tuple:
    return (str(project.get("updated", "")), str(project.get("title", "")))


def human_date(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d.%m.%Y")
    except (TypeError, ValueError):
        return value or ""


def render_card(project: dict) -> str:
    slug = html.escape(str(project["slug"]), quote=True)
    title = html.escape(str(project.get("title") or project["slug"]), quote=True)
    description = html.escape(str(project.get("description", "")), quote=True)
    tags = [str(t) for t in project.get("tags", []) if str(t).strip()]
    path = html.escape(str(project.get("path") or f"projects/{project['slug']}/index.html"), quote=True)
    updated = str(project.get("updated", ""))
    search = " ".join([title, description, " ".join(tags)]).lower()
    search_attr = html.escape(search, quote=True)

    tag_html = "\n".join(
        f'                <span class="tag">#{html.escape(tag, quote=True)}</span>' for tag in tags
    )
    if not tag_html:
        tag_html = '                <span class="tag">#проект</span>'

    return f'''          <article class="card" data-search="{search_attr}">
            <div class="card__top">
              <span class="card__slug">{slug}</span>
              <time class="card__date" datetime="{html.escape(updated, quote=True)}">{human_date(updated)}</time>
            </div>
            <h2 class="card__title"><a href="{path}">{title}</a></h2>
            <p class="card__desc">{description}</p>
            <div class="card__tags">
{tag_html}
            </div>
            <div class="card__actions">
              <a class="button button--primary" href="{path}">Открыть →</a>
              <button class="button button--ghost" type="button" data-copy="{path}">Скопировать ссылку</button>
            </div>
          </article>'''


def main() -> None:
    projects = sorted(load_projects(), key=sort_key, reverse=True)
    cards = "\n".join(render_card(p) for p in projects)
    if not cards:
        cards = "          <!-- Пока нет проектов: добавьте запись в projects.json -->"

    if not INDEX.exists():
        raise SystemExit(f"index.html not found: {INDEX}")

    text = INDEX.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit(f"Markers {START} / {END} not found in index.html")

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    replacement = f"{START}\n{cards}\n          {END}"
    new_text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit("Could not replace the projects block")
    INDEX.write_text(new_text, encoding="utf-8")
    print(f"Rendered {len(projects)} project(s) into index.html")


if __name__ == "__main__":
    main()
