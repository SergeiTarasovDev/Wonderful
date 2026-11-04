# Wonderful Pages

Витрина проектов: **https://sergeitarasovdev.github.io/Wonderful/**

Одна общая страница и отдельная страница под каждый проект. Старые страницы не удаляются — каждый проект живёт в своём подпроекте.

## Что внутри

| Путь | Что это |
|---|---|
| `index.html` | витрина: карточки проектов, поиск, копирование ссылок |
| `projects/<slug>/index.html` | страница конкретного проекта |
| `projects.json` | манифест: название, описание, теги, дата, источник |
| `tools/add_project.py` | добавить или обновить проект в манифесте |
| `tools/render_projects.py` | перегенерировать карточки в `index.html` |

## Добавить страницу

1. Скопировать HTML в `projects/<slug>/index.html`. Если страница ссылается на локальные ассеты (картинки, CSS, JS), скопировать их рядом с сохранением относительных путей.
2. Обновить манифест и карточки:

   ```powershell
   python tools\add_project.py --slug my-page --title "Моя страница" --description "Короткое описание" --tags "тег1,тег2" --source "откуда взялось"
   ```

3. Закоммитить и запушить:

   ```powershell
   git add -A
   git commit -m "Add page: my-page"
   git push origin main
   ```

Ссылка на страницу:

```text
https://sergeitarasovdev.github.io/Wonderful/projects/my-page/index.html
```

## Существующие проекты

- `projects/wonderful/` — личный трекер задач Wonderful. Демо: https://sergeitarasovdev.github.io/Wonderful/projects/wonderful/

## Автоматизация

Skill `wonderful-pages` (`_Skills\wonderful-pages`) делает всё это одной командой: копирует HTML, обновляет манифест, перегенерирует витрину, коммитит и пушит.
