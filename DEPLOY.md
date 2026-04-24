# Deploy & customize

## Updating the live site

The repo is a GitHub user site, so anything pushed to `main` goes live at `https://jessicango.github.io/` within ~60 seconds.

```bash
cd portfolio-site-v2
git add .
git commit -m "your message"
git push
```

Watch the deploy in the repo's **Actions** tab — the "pages build and deployment" workflow shows green when it's live.

## First-time setup

If setting up a fresh clone or starting from scratch:

```bash
cd portfolio-site-v2
git init -b main
git add .
git commit -m "initial portfolio"
git remote add origin git@github.com:JessicaNgo/JessicaNgo.github.io.git
git push -u origin main
```

Then in the repo: **Settings → Pages → Source: "Deploy from a branch" → `main` / `/ (root)`** (usually already the default). First build can take a few minutes; later pushes deploy within a minute.

### Using a project repo instead of a user site

Push this folder to any repo name (e.g. `portfolio`), enable Pages on `main`, and it serves at `https://jessicango.github.io/portfolio/`. No other changes needed — the site uses relative paths.

## Customizing

- **Tweak colors**: the top of the `<style>` block in `index.html` has CSS variables (`--gold`, `--mint`, `--magenta`, etc). Change them there and every matching element updates. Light-mode overrides live in the `body.light-theme { ... }` block near the end of the stylesheet.
- **Make clean view the default**: in `readView()` (inside the `<script>` block), return `'clean'` when no `?view=` param is present.
- **Force a theme regardless of OS**: in `readTheme()`, replace the `matchMedia` fallback with a hardcoded `return 'dark'` (or `'light'`).
- **Add analytics**: paste your provider's snippet (Plausible, Umami, etc.) right before `</body>`.
- **Custom domain**: add a `CNAME` file at the repo root containing just your domain (e.g. `jessicango.dev`), then set up the DNS records per [GitHub's custom domain docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site). Pages auto-provisions an HTTPS cert via Let's Encrypt.
