# Migration Notes — Quartz → ten-site

Recon performed 2026-06-17 on CT 124 (10.0.1.87 / macxpox).

## Web server

nginx på port 80. Config: `/etc/nginx/sites-enabled/ten`.
Root pekar på `/opt/quartz/public`. **Ska ändras till `/opt/ten-site/public`** i step 9.
Inga HTTPS/TLS — trafiken termineras upstream (Cloudflare Tunnel / proxy).

## Quartz config (quartz.config.ts)

- Umami: websiteId `bc585229-b7c7-4acc-946c-ac3973020601`, host `https://umami.formatet.se` (före 2026-09-23: `s.kristall.info`)
- Typografi: EB Garamond (header + body), JetBrains Mono (code) — self-hosted woff2
- Färger: light mode tvingat (`saved-theme="dark"` overrideas). Papper `#F4EFE3`, bläck `#1a1a1a`.
- SPA aktivt i Quartz (enableSPA: true) — i nya sajten ingen SPA, vanliga sidladdningar.

## Quartz layout (quartz.layout.ts)

Nav-ordning: CHAPTERS → THE-GALLERY → THE-ARCHIVE (definierad via `FOLDER_ORDER`-array i explorerSort).
Explorer: `folderClickBehavior: "collapse"`, `useSavedState: false`.
Vänster sidebar: PageTitle (logotyp), Search, Explorer.
Höger sidebar: TableOfContents (desktop only).
afterBody: Backlinks, WiktionaryLookup, TENTracking.

## Design-tokens (porterade till site.css)

| Token | Värde |
|---|---|
| --paper | #F4EFE3 |
| --ink | #1a1a1a |
| --ink-light | #2A2826 |
| --gray | #6B6760 |
| --rule | rgba(26,26,26,0.18) |
| --rule-mid | rgba(26,26,26,0.10) |
| Font | EB Garamond 400/400i |
| font-size | 1.0625rem (~17px) |
| line-height | 1.65 |
| max-width | 65ch (article) |
| sidebar-width | 300px (Quartz: 320px) |
| mobile bp | 800px |
| desktop bp | 1200px |

## Komponenter (porterade till vanilla JS)

- **WiktionaryLookup.tsx** → `static/js/wiktionary.js`
  - Trigger: mouseup/touchend → getSelection() → ord utan mellanrum, 2–30 tecken
  - Tooltip: fixed, `#wikt-tip`, `transform: translateX(-50%)`, triangelpil nedåt
  - Umami-event: `wiktionary { word: clean }`
- **TENTracking.tsx** → `static/js/tracking.js`
  - scroll-depth 25/50/75/100% med `{ pct, page }`
  - nav-explorer `{ to: href }`; nav-toc `{ section }`
  - external-link `{ url }` (ej wiktionary)
  - time-on-page `{ secs, page }` vid beforeunload (>5 sek)
  - search `{ q }` med 600ms debounce

## Statiska filer (kopierade)

Fonter och logotyper kopierade från `/opt/quartz/quartz/static/` till `static/`:
- `fonts/eb-garamond-regular.woff2`
- `fonts/eb-garamond-italic-400.woff2`
- `img/ten-logo-monogram.svg` (180×95 effective, SVG art 490×258)
- `img/ten-logo-horizontal.svg`, `ten-logo-inverted.svg`, `ten-logo-primary.svg`
- `img/favicon.svg`

## Innehållsstruktur på CT 124 (per 2026-06-17)

```
/opt/quartz/content/
├── index.md                          # student-facing homepage
├── The Gallery.md                    # gallery stub (ersätts av content/gallery/index.md)
├── CHAPTERS/
│   ├── Chapter N Title – Full.md     # elevtext (dessa migreras)
│   ├── Title.md                      # korta stubbar (ignoreras)
│   └── lesson-schedule.md            # intern (ignoreras)
├── THE GALLERY/
│   └── Name.md                       # 33 individuella porträtt
└── THE ARCHIVE/
    ├── Chapter N.md                  # etymologi per kapitel
    ├── Alphabetical Index.md
    └── ...
```

## Gammal platt HTML-gallery (fråga 2)

Fil: `/opt/quartz/public/The-Gallery.html` — detta är byggartefakten av `The Gallery.md`.
Det finns INTE en fristående manuellt skapad HTML-gallerifil. Filen är genererad av Quartz
från The Gallery.md och försvinner när vi slutar bygga med Quartz.
Ingen separat städning behövs — bygg ny sajt, peka om nginx, klar.

## Gitea-repo

`formatet/ten-site` fanns inte i Gitea per 2026-06-17.
Timothy skapar repot via http://10.0.1.67:3000 och lägger till remote:
```bash
cd /opt/ten-site
git remote add ten ssh://git@10.0.1.67:2222/formatet/ten-site.git
git push ten main
```

## Nginx-switch (step 9)

```nginx
# Ändra i /etc/nginx/sites-enabled/ten:
root /opt/ten-site/public;   # var: /opt/quartz/public
```
Sedan: `nginx -t && systemctl reload nginx`
