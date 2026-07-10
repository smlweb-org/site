# S—ML Web · site

Source of **[smlweb.org](https://smlweb.org)** — the public home of the S—ML Web standard.

This site is its own reference implementation: Sparse-conformant pages. No JavaScript required (the theme toggle is CSS-only), no third-party requests, system mono fonts, inline styles — verified with [`sml-audit`](https://github.com/smlweb-org/sml-audit). View source; that is the point.

**No duplicated content.** The site hosts nothing that lives elsewhere: downloads link to the canonical GitHub repositories (`spec`, `sml-audit`, `skills`), so every link always points at the current version. The only generated artifacts here are the HTML readers and `llms-full.txt`, built from `../spec` at build time.

## Contents

- `index.html` — the landing page. Edit and deploy.
- `spec/index.html`, `paper/index.html` — human-readable HTML readers, generated from the canonical Markdown in the sibling `spec` repo (see below).
- `build-docs.py` — zero-dependency script that builds the HTML readers from `../spec/spec.md` and `../spec/paper.md`.
- `llms.txt` — curated map for AI crawlers (physical file at the root, by convention).
- `llms-full.txt` — flattened spec text; regenerate when the spec changes.
- `robots.txt`, `sitemap.xml` — with AI crawlers explicitly allowed.
- `_headers` — sets `Content-Profile: s`, `Available-Profiles: s`, `Vary: Accept-Profile` on Netlify/Cloudflare Pages.
- `_redirects` — legacy paths (`/spec.md`, `/downloads/*`, tool zips) forward to the canonical GitHub locations.

## Build

This repo expects its siblings checked out alongside it (as in the project root):

```
smlweb/
├── spec/       ← canonical spec.md + paper.md (source for the readers)
├── sml-audit/  ← auditor used by local checks
└── site/       ← this repo
```

After the spec or paper changes in `../spec`, regenerate:

```bash
python3 build-docs.py                                  # rebuilds spec/ and paper/ readers
# and refresh the flattened LLM text:
{ echo "# S—ML Web — full text for LLMs"; echo; \
  echo "Source: https://smlweb.org/ · Canonical: https://github.com/smlweb-org/spec · License: CC BY 4.0"; echo; \
  cat ../spec/spec.md; } > llms-full.txt
```

Commit the generated HTML with the change.

## Run locally

```bash
python3 -m http.server 8080
# then open http://localhost:8080
```

## Deploy notes

Any static host works. On Cloudflare, disable the default AI-crawler blocking (it overrides robots.txt at the edge). External redirects in `_redirects` (to github.com) are supported by Netlify and Cloudflare Pages.

## Local checks

```bash
node ../sml-audit/sml-audit.js http://localhost:8080/ --profile=s          # home — must PASS
node ../sml-audit/sml-audit.js http://localhost:8080/spec/ --profile=s     # spec reader
node ../sml-audit/sml-audit.js http://localhost:8080/paper/ --profile=s    # paper reader
```

A PR that pushes any page over its Sparse budget fails review by definition — the budgets are the site's own contract.

## License

Content CC BY 4.0 · code MIT.
