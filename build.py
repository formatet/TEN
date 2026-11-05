#!/usr/bin/env python3
"""
Minimal static site generator for ten.formatet.se.
stdlib only (imports lib/markdown2 which is vendored).
Usage: python3 build.py
"""

import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
import markdown2

from nav import NAV, section_for_href

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
PUBLIC  = os.path.join(ROOT, "public")
STATIC  = os.path.join(ROOT, "static")
TEMPLATE_FILE = os.path.join(ROOT, "templates", "base.html")

MARKDOWN_EXTRAS = ["tables", "fenced-code-blocks", "header-ids", "break-on-newline"]

# Texts moved under their author's Gallery page (2026-10-02)
REDIRECTS = {
    "/gallery/if/":               "/gallery/rudyard-kipling/if/",
    "/gallery/rikki-tikki-tavi/": "/gallery/rudyard-kipling/rikki-tikki-tavi/",
}


# ─── Frontmatter ────────────────────────────────────────────────────────────

def parse_frontmatter(text):
    """Parse simple YAML-ish frontmatter. Returns (meta_dict, body_str)."""
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
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        meta[key] = val
    return meta, body


# ─── Callout preprocessor ───────────────────────────────────────────────────

CALLOUT_RE = re.compile(
    r'^> \[!(\w+)\][ \t]*(.*?)\n((?:^>.*\n?)*)',
    re.MULTILINE
)


def expand_callouts(text):
    """Convert Obsidian callout syntax to HTML aside blocks."""
    def replace(m):
        kind  = m.group(1).lower()
        title = m.group(2).strip()
        body_lines = m.group(3)
        inner = re.sub(r'^> ?', '', body_lines, flags=re.MULTILINE).strip()
        inner_html = markdown2.markdown(inner, extras=MARKDOWN_EXTRAS)
        title_html = f'<p class="callout-title">{title}</p>\n' if title else ''
        return (
            f'<aside class="callout callout-{kind}">\n'
            f'{title_html}'
            f'{inner_html}'
            f'</aside>\n\n'
        )
    return CALLOUT_RE.sub(replace, text)


# ─── TOC generation ─────────────────────────────────────────────────────────

def build_toc(html):
    """Extract h2/h3 from rendered HTML and return the page-index rail.

    The rail sits in the right column on wide screens and collapses to a
    Contents box above the article on narrower ones — same markup, placed by
    the grid in site.css.
    """
    headings = re.findall(r'<h([23])[^>]*id="([^"]*)"[^>]*>(.*?)</h\1>', html, re.DOTALL)
    if len(headings) < 2:
        return ""
    items = []
    for level, hid, text in headings:
        clean = re.sub(r'<[^>]+>', '', text).strip()
        cls = "toc-h3" if level == "3" else ""
        if level == "2" and clean.startswith("Part "):
            cls = "toc-part"
        items.append(f'<li class="{cls}"><a href="#{hid}">{clean}</a></li>')
    return (
        '  <aside class="toc-rail" aria-label="On this page">\n'
        '<details class="toc" open>\n'
        '<summary>Contents</summary>\n'
        '<ol>\n'
        + '\n'.join(items) +
        '\n</ol>\n</details>\n'
        '  </aside>\n'
    )


# ─── Nav rendering ──────────────────────────────────────────────────────────

def render_nav(current_href):
    """Render sidebar nav; open only the section of the current page."""
    current_section = section_for_href(current_href)
    parts = []
    for section in NAV:
        open_attr = ' open' if section["id"] == current_section else ''
        items_html = []
        for item in section["items"]:
            active = ' class="active"' if item["href"] == current_href else ''
            items_html.append(
                f'      <li><a href="{item["href"]}"{active}>{item["title"]}</a></li>'
            )
        parts.append(
            f'  <details{open_attr}>\n'
            f'    <summary>{section["title"]}</summary>\n'
            f'    <ul>\n'
            + '\n'.join(items_html) + '\n'
            f'    </ul>\n'
            f'  </details>'
        )
    return '\n'.join(parts)


# ─── Page rendering ─────────────────────────────────────────────────────────

def render_page(meta, body, current_href, template):
    """Render a single page to HTML string."""
    preprocessed = expand_callouts(body)
    content_html  = markdown2.markdown(preprocessed, extras=MARKDOWN_EXTRAS)
    toc_html      = build_toc(content_html)
    nav_html      = render_nav(current_href)
    title         = meta.get("title", "")

    html = (
        template
        .replace("${page_title}", title)
        .replace("${nav_html}", nav_html)
        .replace("${content_html}", content_html)
        .replace("${toc_html}", toc_html)
    )
    return html, content_html


# ─── Output path ────────────────────────────────────────────────────────────

def href_for_content_path(rel_path):
    """Convert content/foo/bar.md → /foo/bar/"""
    rel_path = rel_path.replace("\\", "/")
    parts = rel_path.split("/")
    # Strip .md, handle index.md specially
    stem = parts[-1]
    if stem == "index.md":
        parts = parts[:-1]
    else:
        parts[-1] = stem[:-3]  # remove .md
    return "/" + "/".join(parts) + "/" if parts else "/"


def output_path_for_href(href):
    """Convert /foo/bar/ → public/foo/bar/index.html"""
    if href == "/":
        return os.path.join(PUBLIC, "index.html")
    parts = href.strip("/").split("/")
    return os.path.join(PUBLIC, *parts, "index.html")


# ─── Search index ───────────────────────────────────────────────────────────

def strip_html(html):
    return re.sub(r'<[^>]+>', ' ', html).strip()


# ─── Build ──────────────────────────────────────────────────────────────────

def build():
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(PUBLIC)

    # Copy static assets
    shutil.copytree(STATIC, os.path.join(PUBLIC, "static"))

    with open(TEMPLATE_FILE, encoding="utf-8") as f:
        template = f.read()

    search_index = []
    page_count = 0

    # Walk content in sorted order for determinism
    for dirpath, dirnames, filenames in os.walk(CONTENT):
        dirnames.sort()
        for fname in sorted(filenames):
            if not fname.endswith(".md"):
                continue
            full_path = os.path.join(dirpath, fname)
            rel_path  = os.path.relpath(full_path, CONTENT)

            with open(full_path, encoding="utf-8") as f:
                raw = f.read()

            meta, body = parse_frontmatter(raw)

            # Skip non-published or teacher-only files
            if meta.get("publish", "true").lower() == "false":
                continue
            if "teacher" in meta.get("cssclasses", "").lower():
                continue

            current_href = href_for_content_path(rel_path)
            html, content_html = render_page(meta, body, current_href, template)

            out = output_path_for_href(current_href)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                f.write(html)

            page_count += 1

            # The 404 page is a destination, not content — keep it out of search.
            if current_href == "/404/":
                continue

            # Collect for search index (reuse already-rendered HTML).
            # The whole page is indexed — truncating meant a search for a word
            # in the second half of a chapter returned nothing.
            plain = re.sub(r'\s+', ' ', strip_html(content_html))
            search_index.append({
                "title": meta.get("title", fname),
                "href": current_href,
                "text": plain,
            })

    # Old URLs that may already be shared with students → redirect stubs
    for old, new in REDIRECTS.items():
        out = output_path_for_href(old)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={new}">'
                    f'<link rel="canonical" href="{new}"><a href="{new}">{new}</a>\n')

    # Write search index
    idx_path = os.path.join(PUBLIC, "static", "search-index.json")
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump(search_index, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Built {page_count} pages → public/")


if __name__ == "__main__":
    build()
