# zalakbhojani.github.io

Personal site of Zalak Bhojani, built with [Hugo](https://gohugo.io/) and
deployed to GitHub Pages via GitHub Actions.

**Live at: https://zalakbhojani.github.io/**

## How this repo is wired (read this first)

- **Site config, life events, and the Substack feed snapshot live here.**
- **Page content and templates live in the theme submodule** at `themes/mini`
  — a private fork: [`hugo-theme-mini-zbhojani`](https://github.com/ZalakBhojani/hugo-theme-mini-zbhojani).
  The homepage bio (`layouts/partials/info.html`), the about page, and all
  section templates are in there. Changing them means: commit + push in the
  submodule, then commit the submodule pointer bump here.
- This repo **must stay public** — GitHub Pages on the free plan does not
  publish private repos (that is what took the site down in the past).

## Common tasks

### Add a life event (the "Life" page, `/stream`)

Edit [`data/stream.yaml`](data/stream.yaml) — newest entry on top:

```yaml
- date: Mar 2026          # freeform display text
  text: Something happened  # markdown ok
  link: https://example.com # optional, renders a small arrow
```

Commit and push. No submodule involved.

### Published a new Substack post?

```bash
./scripts/refresh-feed.sh
```

`/blogs` is an on-site index of the Substack feed (https://zalakb.substack.com).
Substack's CDN blocks GitHub Actions IPs, so CI cannot fetch the feed itself;
a snapshot is committed at `assets/substack-feed.xml` and this script
refreshes it, commits, and pushes (deploys automatically). CI still tries a
best-effort refresh on every build in case Substack ever unblocks Actions.

### Change the bio / homepage text

Edit `themes/mini/layouts/partials/info.html`, then:

```bash
cd themes/mini
git checkout main && git commit -am "Update bio" && git push
cd ../..   # back to site repo
git commit -am "Bump theme" themes/mini && git push
```

## Local development

```bash
git clone --recurse-submodules git@github.com:ZalakBhojani/ZalakBhojani.github.io.git
hugo server        # http://localhost:1313
```

The submodule is private — cloning it needs credentials for the
`ZalakBhojani` account. Built with Hugo extended 0.115.4 (version pinned in
`.github/workflows/hugo.yaml`).

## Deployment

Push to `main` → `.github/workflows/hugo.yaml` builds and deploys.
Also runs weekly (Mon 06:00 UTC) and via manual dispatch.
Pages source is set to **GitHub Actions** (repo Settings → Pages).

### Things that will break the site silently one day

- **The `PAT` repo secret expires ~Sept 2027.** It is a fine-grained token
  with read access to this repo and the theme fork (needed because the fork
  is private). When it expires, every deploy fails at checkout. Renew at
  GitHub → Settings → Developer settings → Fine-grained tokens, then update
  the secret: `gh secret set PAT --repo ZalakBhojani/ZalakBhojani.github.io`.
  (Making the theme fork public removes this failure mode entirely.)
- **Scheduled workflows get disabled after ~60 days without repo activity.**
  GitHub emails a warning; one click re-enables.
- **Making this repo private unpublishes the site** (free plan).
