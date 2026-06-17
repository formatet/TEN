#!/usr/bin/env python3
"""
One-shot migration: vault markdown → content/ (repo markdown).

Run from the ten-site repo root:
  python3 migrate.py

Reads from VAULT_DIR, writes to content/. Converts [[wikilinks]] to regular
markdown links. Logs unresolved wikilinks. Does NOT run build.py.
"""

import os
import re
import sys
import unicodedata

VAULT = os.path.expanduser("~/Dokument/myltavault")
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(REPO_ROOT, "content")

# ─── Slug helpers ────────────────────────────────────────────────────────────

def slugify(name):
    """Convert a display name to a URL slug."""
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    name = name.lower()
    name = re.sub(r"['\.]", "", name)
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")


# ─── Known slug map: vault filename → URL path ───────────────────────────────
# Build this from the known content structure so wikilinks can resolve.

SLUG_MAP = {}

def build_slug_map():
    global SLUG_MAP

    # Chapters
    for n, title in [
        (1, "The Foundational Narrative"),
        (2, "The Music of the Image"),
        (3, "The American Document"),
        (4, "The Rhetoric of Power"),
        (5, "The Post-Colonial Witness"),
        (6, "The Anatomy of Irony"),
        (7, "The Fragmented Self"),
        (8, "The Weight of History"),
        (9, "The Final Synthesis"),
    ]:
        vault_name = f"Chapter {n} {title} – Full"
        href = f"/chapters/{n}-{slugify(title)}/"
        SLUG_MAP[vault_name] = href
        SLUG_MAP[f"Chapter {n} {title}"] = href

    # Gallery portraits — map both "Name" and "Name (year–year)" variants
    gallery_names = [
        "Abdulrazak Gurnah", "Alice Munro", "Bertrand Russell", "Bob Dylan",
        "Derek Walcott", "Doris Lessing", "Ernest Hemingway", "Eugene O'Neill",
        "George Bernard Shaw", "Harold Pinter", "J.M. Coetzee", "John Galsworthy",
        "John Steinbeck", "Joseph Brodsky", "Kazuo Ishiguro", "Louise Glück",
        "Nadine Gordimer", "Patrick White", "Pearl S. Buck", "Rabindranath Tagore",
        "Rudyard Kipling", "Samuel Beckett", "Saul Bellow", "Seamus Heaney",
        "Sinclair Lewis", "T.S. Eliot", "Toni Morrison", "V.S. Naipaul",
        "W.B. Yeats", "William Faulkner", "William Golding", "Winston Churchill",
        "Wole Soyinka",
    ]
    for name in gallery_names:
        slug = slugify(name)
        href = f"/gallery/{slug}/"
        SLUG_MAP[name] = href
        # Also match with year suffix e.g. "Pearl S. Buck (1892–1973)"
        SLUG_MAP[re.sub(r'\s*\(\d.*\)$', '', name).strip()] = href

    # Gallery index
    SLUG_MAP["The Gallery"] = "/gallery/"
    SLUG_MAP["THE GALLERY"] = "/gallery/"

    # Archive
    for n in range(1, 10):
        SLUG_MAP[f"Etymologi – Kapitel {n}"] = f"/archive/chapter-{n}/"
        SLUG_MAP[f"Chapter {n}"] = f"/archive/chapter-{n}/"
    SLUG_MAP["The Etymological Archive"] = "/archive/"
    SLUG_MAP["Etymologiska arkivet – Alfabetiskt index"] = "/archive/alphabetical-index/"
    SLUG_MAP["Alphabetical Index"] = "/archive/alphabetical-index/"
    SLUG_MAP["Etymologi – Det normanska skiftet"] = "/archive/"


build_slug_map()

# ─── Wikilink conversion ─────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
unresolved_log = []


def convert_wikilinks(text, source_file):
    def replace(m):
        target = m.group(1).strip()
        label  = (m.group(2) or m.group(1)).strip()
        href   = SLUG_MAP.get(target)
        if href:
            return f"[{label}]({href})"
        unresolved_log.append(f"  [{source_file}] [[{target}]]")
        return f"[{label}]({target})"  # keep as broken link — fix manually
    return WIKILINK_RE.sub(replace, text)


# ─── Frontmatter helpers ─────────────────────────────────────────────────────

def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_block = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    meta = {}
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta, body


KEEP_KEYS = {"title", "order", "publish", "section"}

def clean_frontmatter(meta):
    """Keep only fields relevant to the new build system."""
    out = {k: v for k, v in meta.items() if k in KEEP_KEYS}
    return out


def write_frontmatter(meta):
    lines = ["---"]
    for k, v in meta.items():
        lines.append(f'{k}: "{v}"')
    lines.append("---\n")
    return "\n".join(lines)


# ─── File readers ────────────────────────────────────────────────────────────

def read_vault(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def should_migrate(meta):
    if meta.get("publish", "").lower() == "false":
        return False
    css = meta.get("cssclasses", "").lower()
    if "teacher" in css:
        return False
    return True


def write_content(dest_path, meta, body, source_file):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    body = convert_wikilinks(body, source_file)
    cleaned_meta = clean_frontmatter(meta)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(write_frontmatter(cleaned_meta))
        f.write(body)


# ─── Migration tasks ─────────────────────────────────────────────────────────

def migrate_chapters():
    count = 0
    for n in range(1, 10):
        titles = {
            1: "The Foundational Narrative",
            2: "The Music of the Image",
            3: "The American Document",
            4: "The Rhetoric of Power",
            5: "The Post-Colonial Witness",
            6: "The Anatomy of Irony",
            7: "The Fragmented Self",
            8: "The Weight of History",
            9: "The Final Synthesis",
        }
        title = titles[n]
        src = os.path.join(VAULT, f"Chapter {n} {title} – Full.md")
        slug = slugify(title)
        dest = os.path.join(CONTENT, "chapters", f"{n}-{slug}.md")
        if not os.path.exists(src):
            print(f"  WARNING: chapter source not found: {src}")
            continue
        raw = read_vault(src)
        meta, body = parse_frontmatter(raw)
        if not should_migrate(meta):
            print(f"  SKIP (teacher/unpublished): Chapter {n}")
            continue
        meta.setdefault("title", title)
        meta["order"] = str(n)
        write_content(dest, meta, body, f"chapters/{n}-{slug}.md")
        print(f"  chapter {n}: {title}")
        count += 1
    return count


def migrate_gallery():
    count = 0
    gallery_dir = os.path.join(VAULT, "THE GALLERY")
    if not os.path.isdir(gallery_dir):
        print(f"  WARNING: gallery dir not found: {gallery_dir}")
        return 0
    for fname in sorted(os.listdir(gallery_dir)):
        if not fname.endswith(".md"):
            continue
        src = os.path.join(gallery_dir, fname)
        raw = read_vault(src)
        meta, body = parse_frontmatter(raw)
        if not should_migrate(meta):
            continue
        name = fname[:-3]  # strip .md
        # Strip year suffix from title if present: "Pearl S. Buck (1892–1973)" → use as-is for title
        title = meta.get("title", name)
        slug = slugify(re.sub(r'\s*\(\d.*\)$', '', name).strip())
        dest = os.path.join(CONTENT, "gallery", f"{slug}.md")
        write_content(dest, meta, body, f"gallery/{slug}.md")
        print(f"  gallery: {name}")
        count += 1

    # Gallery index page
    gallery_index_src = os.path.join(VAULT, "The Gallery.md") if os.path.exists(
        os.path.join(VAULT, "The Gallery.md")) else None
    if gallery_index_src:
        raw = read_vault(gallery_index_src)
        meta, body = parse_frontmatter(raw)
    else:
        meta = {"title": "The Gallery", "publish": "true"}
        body = (
            "The dictation portraits — one per laureate, in alphabetical order. "
            "Each portrait is ~150 words and doubles as a dictation text.\n"
        )
    dest = os.path.join(CONTENT, "gallery", "index.md")
    write_content(dest, meta, body, "gallery/index.md")
    print("  gallery: index")
    count += 1
    return count


def migrate_archive():
    count = 0
    # Individual chapter archive files
    for n in range(1, 10):
        src = os.path.join(VAULT, f"Etymologi – Kapitel {n}.md")
        if not os.path.exists(src):
            print(f"  WARNING: archive chapter {n} not found: {src}")
            continue
        raw = read_vault(src)
        meta, body = parse_frontmatter(raw)
        if not should_migrate(meta):
            continue
        # Override title to English
        meta["title"] = f"Chapter {n}"
        meta["order"] = str(n)
        dest = os.path.join(CONTENT, "archive", f"chapter-{n}.md")
        write_content(dest, meta, body, f"archive/chapter-{n}.md")
        print(f"  archive: chapter {n}")
        count += 1

    # Alphabetical index
    src = os.path.join(VAULT, "Etymologiska arkivet – Alfabetiskt index.md")
    if os.path.exists(src):
        raw = read_vault(src)
        meta, body = parse_frontmatter(raw)
        meta["title"] = "Alphabetical Index"
        dest = os.path.join(CONTENT, "archive", "alphabetical-index.md")
        write_content(dest, meta, body, "archive/alphabetical-index.md")
        print("  archive: alphabetical-index")
        count += 1

    # Archive index
    src = os.path.join(VAULT, "The Etymological Archive.md") if os.path.exists(
        os.path.join(VAULT, "The Etymological Archive.md")) else None
    if src:
        raw = read_vault(src)
        meta, body = parse_frontmatter(raw)
    else:
        meta = {"title": "The Archive", "publish": "true"}
        body = (
            "The Etymological Archive tracks every bolded word across all nine chapters. "
            "Use it as a thinking tool, not a vocabulary list.\n"
        )
    dest = os.path.join(CONTENT, "archive", "index.md")
    write_content(dest, meta, body, "archive/index.md")
    print("  archive: index")
    count += 1
    return count


def migrate_homepage():
    """Use the existing student-facing index from Quartz content/."""
    quartz_index = "/opt/quartz/content/index.md"
    dest = os.path.join(CONTENT, "index.md")
    if os.path.exists(quartz_index):
        raw = read_vault(quartz_index)
        meta, body = parse_frontmatter(raw)
    else:
        meta = {"title": "The English Nobel", "publish": "true"}
        body = "Three years. Nine chapters. Thirty-three writers who changed the language.\n"
    # Fix any Quartz-style internal links that use /THE-GALLERY etc.
    body = body.replace("/THE-GALLERY", "/gallery/")
    body = body.replace("/CHAPTERS", "/chapters/")
    body = body.replace("/THE-ARCHIVE", "/archive/")
    body = convert_wikilinks(body, "index.md")
    write_content(dest, meta, body, "index.md")
    print("  homepage: index.md")
    return 1


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("Migrating vault content to content/…")
    total = 0
    total += migrate_homepage()
    print("\nChapters:")
    total += migrate_chapters()
    print("\nGallery:")
    total += migrate_gallery()
    print("\nArchive:")
    total += migrate_archive()

    print(f"\nTotal: {total} files written.")

    if unresolved_log:
        print(f"\nUnresolved wikilinks ({len(unresolved_log)}) — fix manually:")
        for line in unresolved_log:
            print(line)
    else:
        print("\nAll wikilinks resolved.")


if __name__ == "__main__":
    main()
