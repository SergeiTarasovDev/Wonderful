#!/usr/bin/env python3
"""Add or update a project in projects.json and regenerate the hub cards."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "projects.json"
PUBLIC_BASE = "https://sergeitarasovdev.github.io/Wonderful"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add or update a Wonderful Pages project")
    parser.add_argument("--slug", required=True, help="ASCII slug, e.g. pds-pension")
    parser.add_argument("--title", required=True, help="Human-readable title")
    parser.add_argument("--description", default="", help="Short description")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--source", default="", help="Where the page came from")
    parser.add_argument("--updated", default=date.today().isoformat(), help="YYYY-MM-DD")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    slug = args.slug.strip().lower()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise SystemExit("slug must be ASCII lowercase words separated by hyphens")

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    projects: list[dict] = []
    if MANIFEST.exists():
        with MANIFEST.open(encoding="utf-8") as f:
            projects = json.load(f)

    entry = {
        "slug": slug,
        "title": args.title.strip(),
        "description": args.description.strip(),
        "tags": tags,
        "path": f"projects/{slug}/index.html",
        "updated": args.updated,
        "source": args.source.strip(),
    }

    replaced = False
    for i, project in enumerate(projects):
        if project.get("slug") == slug:
            projects[i] = entry
            replaced = True
            break
    if not replaced:
        projects.append(entry)

    MANIFEST.write_text(
        json.dumps(projects, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    project_file = ROOT / "projects" / slug / "index.html"
    if not project_file.exists():
        print(f"WARNING: {project_file} does not exist yet; copy the HTML there first")

    subprocess.run([sys.executable, str(ROOT / "tools" / "render_projects.py")], check=True)
    print(f"{'Updated' if replaced else 'Added'}: {slug}")
    print(f"URL: {PUBLIC_BASE}/projects/{slug}/index.html")
    print("Next: git add -A && git commit && git push origin main")


if __name__ == "__main__":
    main()
