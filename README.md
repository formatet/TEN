# TEN

The course text for a three-year English course at Hvitfeldtska gymnasiet, Gothenburg, built around writers who won the Nobel Prize in Literature. Nine chapters, a portrait gallery of thirty-three writers, and an etymological archive.

Live at [ten.formatet.se](https://ten.formatet.se).

The course is a pilot that started in autumn 2026. Chapters open as the classes reach them; the rest are in `content/chapters/` as drafts with `publish: "false"`.

## How it is made

The texts are written with [Claude Code](https://claude.com/claude-code). I decide what each part of the course should do and which texts we read. Claude drafts and revises, and I edit until I can stand behind every sentence. The commit history shows who wrote what.

## How it works

```
content/*.md → build.py → public/ (static HTML) → nginx
```

`build.py` is one Python file with no dependencies beyond the standard library and a vendored copy of [markdown2](https://github.com/trentm/python-markdown2) in `lib/`. It renders the markdown into one HTML template, builds the sidebar from `nav.py`, and writes a search index. A full build takes about a second.

```bash
python3 build.py      # writes public/
```

- `content/`: chapters, gallery portraits, archive
- `nav.py`: the sidebar, one line per entry
- `templates/base.html`: the page shell
- `static/`: CSS, JS (search, Wiktionary lookup, Umami events), fonts, images

Analytics: [Umami](https://umami.is), self-hosted, no cookies.

## What is not here

Teacher material, lesson plans and assessment live elsewhere and are not published. Two of the stories read in chapter 1, by Pearl S. Buck and John Steinbeck, are still in copyright. They are handed out on paper in class and are not in this repository.

## License

- Text in `content/`: [CC BY-SA 4.0](LICENSE). Exceptions: Rudyard Kipling's *Rikki-Tikki-Tavi* and *If—* and the illustrations in `static/img/rikki-*` are in the public domain, and quotations from other writers belong to them.
- Code: [MIT](LICENSE-CODE). `lib/markdown2.py` is MIT, © Trent Mick and ActiveState.
- EB Garamond: SIL Open Font License.
