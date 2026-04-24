# jessicango.github.io

Personal portfolio. Pixel-art RPG arcade with a recruiter-friendly "clean view" toggle, plus light/dark themes. Single HTML file, zero build step.

Live at [jessicango.github.io](https://jessicango.github.io).

## What's in here

```
portfolio-site-v2/
├── index.html        ← the whole site (HTML + CSS + JS inline)
├── .nojekyll         ← tells GitHub Pages not to run Jekyll
├── README.md         ← this file
├── DEPLOY.md         ← deploy + customize
└── assets/
    └── resume.pdf    ← current resume
```

## Two views, two themes

Two independent toggles sit in the top-right, and both work in either view.

**View: Arcade ↔ Clean**

- **Arcade** (default) — pixel-art overworld map, HUD, scenes, scanlines.
- **Clean** — single-column resume-style page. Link: `?view=clean`.

**Theme: Dark ↔ Light**

- **Dark** (default) — neon-on-navy arcade cabinet.
- **Light** — warm daytime palette, including a daytime pixel map.
- Auto-follows the visitor's OS `prefers-color-scheme` on first visit; their choice persists via `localStorage`.
- URL params force a specific theme: `?theme=light` / `?theme=dark`.

Any combination is shareable:

- `/` — arcade, auto theme
- `/?view=clean` — recruiter view
- `/?view=clean&theme=light` — recruiter view, light mode
- `/#trophy` — arcade, deep-linked to trophy room

## Editing content

All content lives as plain HTML inside `index.html`. Look for the big section comments — each scene is marked:

```
<!-- SCENE 0: WORLD MAP        -->
<!-- SCENE 1: ARCHIVES (about) -->
<!-- SCENE 2: QUEST BOARD      -->
<!-- SCENE 3: INVENTORY        -->
<!-- SCENE 4: TROPHY HALL      -->
<!-- SCENE 5: TAVERN (contact) -->
<!-- CLEAN VIEW                -->
```

When you update a job or project, edit it in **both** the arcade scene and the clean view block — the clean view uses the same copy without the RPG chrome.

Common edits:

- **New job** → `<!-- SCENE 2: QUEST BOARD -->`, copy a `.quest-entry` block, then mirror it into the `#clean-view` `.cv-job` section.
- **Update project** → arcade: `.crate` inside `.inv-grid`. Clean: `.cv-proj` inside `.cv-grid`.
- **Swap resume** → replace `assets/resume.pdf` with your latest file. Both views link to it.

## Features

- **Arcade world map + scenes** — overworld, archives, quest board, shop, trophy hall, tavern.
- **Clean toggle** — `?view=clean` + top-right button for recruiters.
- **Keyboard shortcuts (arcade only)** — `1`–`5` to fast-travel, `0` or `h` for map, `/` for a mini-terminal, `?` for help.
- **Hash routing** — every scene has its own URL (`#archives`, `#quest-board`, etc.) so deep links work.
- **Easter eggs** — hidden coins on each scene (collect 5), Konami code unlocks a CS2 HUD, `/` opens a mini-terminal.
- **Mobile responsive** — both views reflow cleanly.
- **No dependencies** — zero npm, zero build. The only external thing is Google Fonts.
- **`prefers-reduced-motion` respected** — animations disable themselves.

## Trade-offs

- Fonts come from Google Fonts (Press Start 2P, VT323, JetBrains Mono). For a fully self-hosted site, download the woff2 files into `assets/fonts/` and swap the `@font-face` declarations.
- The clean view duplicates some copy from the arcade scenes — updating a bullet means updating it in both places. Small price for no build step.

For deployment and customization, see [DEPLOY.md](DEPLOY.md).
