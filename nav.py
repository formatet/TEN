"""Navigation structure for ten.formatet.se — single source of truth."""

NAV = [
    {
        "id": "chapters",
        "title": "CHAPTERS",
        "items": [
            {"title": "1. The Foundational Narrative",  "href": "/chapters/1-the-foundational-narrative/"},
            # {"title": "2. The Music of the Image",       "href": "/chapters/2-the-music-of-the-image/"},  # dold t.o.m. kapitlet startar (2026-09-28)
            # {"title": "3. The American Document",        "href": "/chapters/3-the-american-document/"},  # dold t.o.m. kapitlet startar (2026-09-28)
            # {"title": "4. The Rhetoric of Power",        "href": "/chapters/4-the-rhetoric-of-power/"},  # dold t.o.m. kapitlet startar (2026-09-28)
            # {"title": "5. The Post-Colonial Witness",    "href": "/chapters/5-the-post-colonial-witness/"},  # dold t.o.m. kapitlet startar (2026-09-28)
            # {"title": "6. The Anatomy of Irony",         "href": "/chapters/6-the-anatomy-of-irony/"},  # dold t.o.m. kapitlet startar (2026-09-28)
            # {"title": "7. The Fragmented Self",          "href": "/chapters/7-the-fragmented-self/"},  # dold t.o.m. kapitlet startar (2026-09-28)
            # {"title": "8. The Weight of History",        "href": "/chapters/8-the-weight-of-history/"},  # dold t.o.m. kapitlet startar (2026-09-28)
            # {"title": "9. The Final Synthesis",          "href": "/chapters/9-the-final-synthesis/"},  # dold t.o.m. kapitlet startar (2026-09-28)
        ],
    },
    {
        "id": "gallery",
        "title": "THE GALLERY",
        "items": [
            {"title": "The Gallery",          "href": "/gallery/"},
            {"title": "Abdulrazak Gurnah",    "href": "/gallery/abdulrazak-gurnah/"},
            {"title": "Alice Munro",          "href": "/gallery/alice-munro/"},
            {"title": "Bertrand Russell",     "href": "/gallery/bertrand-russell/"},
            {"title": "Bob Dylan",            "href": "/gallery/bob-dylan/"},
            {"title": "Derek Walcott",        "href": "/gallery/derek-walcott/"},
            {"title": "Doris Lessing",        "href": "/gallery/doris-lessing/"},
            {"title": "Ernest Hemingway",     "href": "/gallery/ernest-hemingway/"},
            {"title": "Eugene O'Neill",       "href": "/gallery/eugene-oneill/"},
            {"title": "George Bernard Shaw",  "href": "/gallery/george-bernard-shaw/"},
            {"title": "Harold Pinter",        "href": "/gallery/harold-pinter/"},
            {"title": "J.M. Coetzee",         "href": "/gallery/jm-coetzee/"},
            {"title": "John Galsworthy",      "href": "/gallery/john-galsworthy/"},
            {"title": "John Steinbeck",       "href": "/gallery/john-steinbeck/"},
            {"title": "Joseph Brodsky",       "href": "/gallery/joseph-brodsky/"},
            {"title": "Kazuo Ishiguro",       "href": "/gallery/kazuo-ishiguro/"},
            {"title": "Louise Glück",         "href": "/gallery/louise-gluck/"},
            {"title": "Nadine Gordimer",      "href": "/gallery/nadine-gordimer/"},
            {"title": "Patrick White",        "href": "/gallery/patrick-white/"},
            {"title": "Pearl S. Buck",        "href": "/gallery/pearl-s-buck/"},
            {"title": "Rabindranath Tagore",  "href": "/gallery/rabindranath-tagore/"},
            {"title": "Rudyard Kipling",      "href": "/gallery/rudyard-kipling/"},
            {"title": "— If—",                "href": "/gallery/if/"},
            {"title": "— Rikki-Tikki-Tavi",   "href": "/gallery/rikki-tikki-tavi/"},
            {"title": "Samuel Beckett",       "href": "/gallery/samuel-beckett/"},
            {"title": "Saul Bellow",          "href": "/gallery/saul-bellow/"},
            {"title": "Seamus Heaney",        "href": "/gallery/seamus-heaney/"},
            {"title": "Sinclair Lewis",       "href": "/gallery/sinclair-lewis/"},
            {"title": "T.S. Eliot",           "href": "/gallery/ts-eliot/"},
            {"title": "Toni Morrison",        "href": "/gallery/toni-morrison/"},
            {"title": "V.S. Naipaul",         "href": "/gallery/vs-naipaul/"},
            {"title": "W.B. Yeats",           "href": "/gallery/wb-yeats/"},
            {"title": "William Faulkner",     "href": "/gallery/william-faulkner/"},
            {"title": "William Golding",      "href": "/gallery/william-golding/"},
            {"title": "Winston Churchill",    "href": "/gallery/winston-churchill/"},
            {"title": "Wole Soyinka",         "href": "/gallery/wole-soyinka/"},
        ],
    },
    {
        "id": "archive",
        "title": "THE ARCHIVE",
        "items": [
            {"title": "The Archive",          "href": "/archive/"},
            {"title": "Chapter 1",            "href": "/archive/chapter-1/"},
            {"title": "Chapter 2",            "href": "/archive/chapter-2/"},
            {"title": "Chapter 3",            "href": "/archive/chapter-3/"},
            {"title": "Chapter 4",            "href": "/archive/chapter-4/"},
            {"title": "Chapter 5",            "href": "/archive/chapter-5/"},
            {"title": "Chapter 6",            "href": "/archive/chapter-6/"},
            {"title": "Chapter 7",            "href": "/archive/chapter-7/"},
            {"title": "Chapter 8",            "href": "/archive/chapter-8/"},
            {"title": "Chapter 9",            "href": "/archive/chapter-9/"},
            {"title": "Alphabetical Index",   "href": "/archive/alphabetical-index/"},
        ],
    },
]


def section_for_href(href):
    """Return section id for a given href, or None if not found."""
    for section in NAV:
        for item in section["items"]:
            if item["href"] == href:
                return section["id"]
    return None
