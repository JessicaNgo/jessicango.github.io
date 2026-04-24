# jessicango.github.io

Personal portfolio site. Pixel-art RPG arcade with a recruiter-friendly "clean view" toggle *and* a light/dark theme toggle. Single-file site, zero build step.

## Quick deploy

1. Create a GitHub repo named `JessicaNgo.github.io` (the repo name matters — this is what makes it a "user site").
2. Copy everything in this folder into the repo root.
3. Commit and push to `main`.
4. GitHub Pages will serve it within a minute at `https://jessicango.github.io`.

```bash
cd portfolio-site-v2
git init
git add .
git commit -m "initial portfolio"
git branch -M main
git remote add origin git@github.com:JessicaNgo/JessicaNgo.github.io.git
git push -u origin main
```

Then in the repo: **Settings → Pages → Source: "Deploy from a branch" → `main` / `/ (root)`** (usually the default).

If you'd rather not use the user-site pattern, put it in any repo (e.g. `portfolio`) and enable GitHub Pages on the `main` branch — it'll serve at `https://jessicango.github.io/portfolio/`.

## File structure

```
portfolio-site-v2/
├── index.html        ← the whole site (HTML + CSS + JS inline)
├── .nojekyll         ← tells GH Pages not to run Jekyll
├── README.md         ← this file
└── assets/
    └── resume.pdf    ← your current resume
```

## Two views, two themes, one file

Two independent toggles live in the top-right corner, both work in either view:

**View: Arcade ↔ Clean**
- **Arcade view (default)** — pixel-art overworld map, HUD, scenes, scanlines, the whole thing.
- **Clean view** — same content as a single-column resume-style page. Link: `?view=clean`.

**Theme: Dark ↔ Light**
- **Dark (default)** — the neon-on-navy arcade cabinet look.
- **Light** — warm daytime palette; pixel-art "game screens" intentionally stay dark (think "arcade cabinet in a sunny room"). Link: `?theme=light`.
- Theme auto-follows the visitor's OS `prefers-color-scheme` on first visit.
- Their choice persists via `localStorage` across visits.
- URL param `?theme=light` / `?theme=dark` forces a specific theme (useful for sharing a link).

Any combination is shareable:
- `https://jessicango.github.io/` — arcade, auto theme
- `https://jessicango.github.io/?view=clean` — recruiter view
- `https://jessicango.github.io/?view=clean&theme=light` — recruiter view, light mode
- `https://jessicango.github.io/?theme=light#trophy` — arcade, light, deep-linked to trophy room

Anyone landing cold can flip views or themes in one click; deep-link hashes (`#about`, `#map`, etc.) keep working in arcade mode.

## Editing content

All the content lives as plain HTML inside `index.html`. Look for the big section comments — each scene is marked:

```
<!-- SCENE 0: WORLD MAP        -->
<!-- SCENE 1: ARCHIVES (about) -->
<!-- SCENE 2: QUEST BOARD      -->
<!-- SCENE 3: INVENTORY        -->
<!-- SCENE 4: TROPHY HALL      -->
<!-- SCENE 5: TAVERN (contact) -->
<!-- CLEAN VIEW                -->
```

When you update a job or project, edit it in **both** the arcade scene and the clean view block. The clean view uses the same copy, just without the RPG chrome.

Common edits:

- **New job** → find `<!-- SCENE 2: QUEST BOARD -->`, copy a `.quest-entry` block, then mirror it into the `#clean-view` `.cv-job` section.
- **Update project** → arcade: `.crate` inside `.inv-grid`. Clean: `.cv-proj` inside `.cv-grid`.
- **Swap resume** → replace `assets/resume.pdf` with your latest file (same filename). Both views link to it.

## Features baked in

- **Arcade world map + scenes** — overworld, archives, quest board, shop, trophy hall, tavern.
- **Clean toggle** — `?view=clean` + top-right button for recruiters who want the resume-shaped version.
- **Keyboard shortcuts (arcade only)** — `1`–`5` to fast-travel, `0` or `h` for map, `/` to summon a mini-terminal, `?` for help. Disabled automatically in clean view.
- **Hash routing** — every scene has its own URL (`#archives`, `#quest-board`, etc.) so deep links work.
- **Easter eggs** — hidden coins on each scene (collect 5), Konami code unlocks a CS2 HUD, `/` opens a mini-terminal.
- **Mobile responsive** — both views reflow cleanly.
- **No dependencies** — zero npm, zero build. Only external thing is Google Fonts.
- **`prefers-reduced-motion` respected** — animations disable themselves.

## Customization tips

- **Tweak colors**: the top of the `<style>` block has CSS variables (`--gold`, `--mint`, `--magenta`, etc). Change them there and every matching element updates. Light-mode overrides live in the `body.light-theme { ... }` block near the end of the stylesheet.
- **Make clean view the default**: swap the default in the `readView()` JS — return `'clean'` when no `?view=` param is present.
- **Force a theme regardless of OS**: in `readTheme()`, replace the `matchMedia` fallback with a hardcoded `return 'dark'` (or `'light'`).
- **Add analytics**: paste your provider's snippet (Plausible, Umami, etc.) right before `</body>`.
- **Custom domain**: add a `CNAME` file at the repo root containing just your domain (e.g. `jessicango.dev`), and set up the DNS records per GitHub's docs.

## Known trade-offs

- Fonts come from Google Fonts (Press Start 2P, VT323, JetBrains Mono). If you want the site fully self-hosted, download the woff2 files, drop them in `assets/fonts/`, and swap the `@font-face` declarations.
- The clean view duplicates some copy from the arcade scenes — when you update a bullet in one, update it in the other. A small price for no build step.
