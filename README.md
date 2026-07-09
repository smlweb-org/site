# S—ML Web · site

Source of **[smlweb.org](https://smlweb.org)** — the public home of the S—ML Web standard.

This site is its own reference implementation: Sparse-conformant pages. No JavaScript required (the theme toggle is CSS-only), no third-party requests, system mono fonts, inline styles — verified with [`sml-audit`](https://github.com/smlweb-org/sml-audit). View source; that is the point.

## Contents

- `index.html` — the landing page. Edit and deploy.
- `spec/index.html`, `paper/index.html` — human-readable HTML readers, generated from the Markdown in `downloads/` (see below).
- `build-docs.py` — zero-dependency script that builds the HTML readers.
- `downloads/` — all distributable files: `spec.md`, `paper.md`, tool zips, skills, `llms.txt`, `llms-full.txt`.
- `sml-audit.js` — local copy of the auditor for development checks (canonical: [smlweb-org/sml-audit](https://github.com/smlweb-org/sml-audit)).
- `robots.txt`, `sitemap.xml` — with AI crawlers explicitly allowed.
- `_headers` — sets `Content-Profile: s`, `Available-Profiles: s`, `Vary: Accept-Profile` on Netlify/Cloudflare Pages.
- `_redirects` — legacy root paths (`/spec.md`, `/llms.txt`, …) forward to `/downloads/`.

## Build HTML readers

After editing `downloads/spec.md` or `downloads/paper.md`, regenerate the reader pages:

```bash
python3 build-docs.py
```

This writes `spec/index.html` and `paper/index.html`. Commit the generated HTML with the source Markdown.

## Run locally

```bash
python3 build-docs.py   # if downloads/*.md changed
python3 -m http.server 8080
# then open http://localhost:8080
```

## Deploy notes

Any static host works. On Cloudflare, disable the default AI-crawler blocking (it overrides robots.txt at the edge). When the spec or tools change in their canonical repos, refresh the files in `downloads/` and re-run `python3 build-docs.py`.

## Local checks

```bash
node sml-audit.js http://localhost:8080/ --profile=s              # home — must PASS
node sml-audit.js http://localhost:8080/spec/ --profile=s         # spec reader
node sml-audit.js http://localhost:8080/paper/ --profile=s        # paper reader
```

A PR that pushes any page over its Sparse budget fails review by definition — the budgets are the site's own contract.

## License

Content CC BY 4.0 · code MIT.
