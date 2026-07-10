#!/usr/bin/env python3
"""Build HTML reader pages from the canonical Markdown in ../spec (single source, no copies). Zero dependencies."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

DOCS = [
    {
        "src": "../spec/spec.md",
        "out": "spec/index.html",
        "title": "S—ML Web Profile 0.4 — Draft Specification",
        "description": "Normative draft spec: profile identifiers, discovery, negotiation, Sparse requirements, budgets, content equivalence, hydration, conformance.",
        "canonical": "https://smlweb.org/spec/",
        "md_alt": "https://github.com/smlweb-org/spec/blob/main/spec.md",
        "nav_active": "spec",
    },
    {
        "src": "../spec/paper.md",
        "out": "paper/index.html",
        "title": "S—ML Web — Position Paper (Draft 0.4)",
        "description": "Full rationale: hydration model, AI consumption, satellite/NTN, aviation, roaming, sustainability, digital balance.",
        "canonical": "https://smlweb.org/paper/",
        "md_alt": "https://github.com/smlweb-org/spec/blob/main/paper.md",
        "nav_active": "paper",
    },
]


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.endswith("|") and s.count("|") >= 2


def is_table_sep(line: str) -> bool:
    s = line.strip().strip("|")
    return bool(s) and all(c in "-:| " for c in s)


def parse_table(lines: list[str], i: int) -> tuple[str, int]:
    rows: list[list[str]] = []
    while i < len(lines) and is_table_row(lines[i]):
        if is_table_sep(lines[i]):
            i += 1
            continue
        cells = [inline_md(c.strip()) for c in lines[i].strip().strip("|").split("|")]
        rows.append(cells)
        i += 1
    body = []
    if not rows:
        return "", i
    header = rows[0]
    body.append("<table>")
    body.append("<thead><tr>" + "".join(f"<th>{c}</th>" for c in header) + "</tr></thead>")
    if len(rows) > 1:
        body.append("<tbody>")
        for row in rows[1:]:
            body.append("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
        body.append("</tbody>")
    body.append("</table>")
    return "\n".join(body), i


def parse_blockquote(lines: list[str], i: int) -> tuple[str, int]:
    parts: list[str] = []
    while i < len(lines) and lines[i].startswith(">"):
        parts.append(lines[i][1:].lstrip())
        i += 1
    inner = "<br>\n".join(inline_md(p) for p in parts)
    return f"<blockquote><p>{inner}</p></blockquote>", i


def parse_list(lines: list[str], i: int, ordered: bool) -> tuple[str, int]:
    items: list[str] = []
    tag = "ol" if ordered else "ul"
    pattern = re.compile(r"^\d+\.\s+" if ordered else r"^[-*]\s+")
    while i < len(lines):
        line = lines[i]
        if pattern.match(line):
            content = pattern.sub("", line, count=1)
            items.append(f"<li>{inline_md(content)}</li>")
            i += 1
        elif line.startswith("  ") and items:
            # continuation line — append to last item (rare in our docs)
            cont = line.strip()
            items[-1] = items[-1][:-5] + " " + inline_md(cont) + "</li>"
            i += 1
        else:
            break
    return f"<{tag}>" + "".join(items) + f"</{tag}>", i


def parse_code(lines: list[str], i: int) -> tuple[str, int]:
    fence = lines[i].strip()
    lang = fence[3:].strip()
    i += 1
    code_lines: list[str] = []
    while i < len(lines) and not lines[i].strip().startswith("```"):
        code_lines.append(lines[i])
        i += 1
    i += 1  # skip closing fence
    code = html.escape("\n".join(code_lines))
    cls = f' class="lang-{html.escape(lang)}"' if lang else ""
    return f"<pre><code{cls}>{code}</code></pre>", i


def md_to_html(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("```"):
            block, i = parse_code(lines, i)
            out.append(block)
            continue

        if is_table_row(line):
            block, i = parse_table(lines, i)
            out.append(block)
            continue

        if line.startswith(">"):
            block, i = parse_blockquote(lines, i)
            out.append(block)
            continue

        if re.match(r"^#{1,3}\s+", line):
            level = len(line) - len(line.lstrip("#"))
            text = line.lstrip("#").strip()
            out.append(f"<h{level}>{inline_md(text)}</h{level}>")
            i += 1
            continue

        if re.match(r"^\d+\.\s+", line):
            block, i = parse_list(lines, i, ordered=True)
            out.append(block)
            continue

        if re.match(r"^[-*]\s+", line):
            block, i = parse_list(lines, i, ordered=False)
            out.append(block)
            continue

        para: list[str] = [line.strip()]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt == "---"
                or nxt.startswith("```")
                or nxt.startswith(">")
                or re.match(r"^#{1,3}\s+", lines[i])
                or re.match(r"^\d+\.\s+", lines[i])
                or re.match(r"^[-*]\s+", lines[i])
                or is_table_row(lines[i])
            ):
                break
            para.append(nxt)
            i += 1
        out.append(f"<p>{inline_md(' '.join(para))}</p>")

    return "\n".join(out)


def shell(doc: dict, body: str) -> str:
    active = doc["nav_active"]
    spec_cls = ' class="active"' if active == "spec" else ""
    paper_cls = ' class="active"' if active == "paper" else ""

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(doc["title"])}</title>
<meta name="description" content="{html.escape(doc["description"])}">
<link rel="canonical" href="{doc["canonical"]}">
<link rel="alternate" type="text/markdown" href="{doc["md_alt"]}" title="Raw Markdown">
<meta name="theme-color" content="#ffffff">
<style>
:root{{
  --bg:#ffffff; --fg:#09090b; --muted:#71717a; --border:#e4e4e7; --card:#fafafa; --invert-bg:#09090b; --invert-fg:#ffffff;
}}
:root:has(#theme:checked){{ --bg:#000000; --fg:#fafafa; --muted:#a1a1aa; --border:#27272a; --card:#0f0f10; --invert-bg:#fafafa; --invert-fg:#09090b; }}
.theme-input{{position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap}}
.theme{{cursor:pointer; color:var(--muted); margin-left:1rem; user-select:none; position:relative; top:-1px; padding-bottom:1px}}
.theme:hover{{color:var(--fg)}}
#theme:focus-visible ~ header .theme{{outline:2px solid var(--fg); outline-offset:3px; border-radius:2px}}
*{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%}}
body{{
  margin:0; background:var(--bg); color:var(--fg);
  font-family:ui-monospace,"IBM Plex Mono",Menlo,Consolas,"Liberation Mono",monospace;
  font-size:14px; line-height:1.65;
}}
main,header.site,footer.site{{max-width:42rem; margin:0 auto; padding:0 1.25rem}}
a{{color:var(--fg); text-underline-offset:3px}}
a:hover{{color:var(--muted)}}
header.site{{display:flex; justify-content:space-between; align-items:baseline; padding-top:1.5rem; padding-bottom:1rem}}
header.site nav a{{margin-left:1rem; text-decoration:none; color:var(--muted)}}
header.site nav a:hover,header.site nav a.active{{color:var(--fg)}}
.wordmark{{font-weight:700; text-decoration:none}}
.muted{{color:var(--muted)}}
pre{{background:var(--card); border:1px solid var(--border); border-radius:8px; padding:1rem 1.25rem; overflow-x:auto; margin:1.25rem 0}}
code{{background:var(--card); border:1px solid var(--border); border-radius:4px; padding:.05rem .35rem}}
pre code{{background:none; border:none; padding:0}}
.prose{{padding:2rem 0 3.5rem}}
.prose h1{{font-size:24px; line-height:1.35; margin:0 0 1.25rem; font-weight:700; letter-spacing:-.02em; color:var(--fg); text-transform:none}}
.prose h2{{font-size:14px; font-weight:700; text-transform:uppercase; letter-spacing:.08em; margin:2.5rem 0 1rem; color:var(--muted)}}
.prose h3{{font-size:14px; font-weight:700; margin:1.75rem 0 .75rem; color:var(--fg); text-transform:none; letter-spacing:0}}
.prose p{{margin:.75rem 0}}
.prose em{{color:var(--muted)}}
.prose hr{{border:none; border-top:1px solid var(--border); margin:2rem 0}}
.prose ul,.prose ol{{margin:.75rem 0; padding-left:1.5rem}}
.prose li{{margin:.35rem 0}}
.prose blockquote{{margin:1.25rem 0; padding:.75rem 1rem; border-left:3px solid var(--border); color:var(--muted)}}
.prose blockquote p{{margin:0}}
.prose table{{width:100%; border-collapse:collapse; margin:1.25rem 0; font-size:13px}}
.prose th,.prose td{{border:1px solid var(--border); padding:.45rem .6rem; text-align:left; vertical-align:top}}
.prose th{{background:var(--card); font-weight:700}}
footer.site{{padding-top:2rem; padding-bottom:3.5rem; border-top:1px solid var(--border); color:var(--muted)}}
footer.site a{{color:var(--muted)}}
:focus-visible{{outline:2px solid var(--fg); outline-offset:2px; border-radius:2px}}
::selection{{background:var(--fg); color:var(--bg)}}
@media (max-width:600px){{ .prose table{{font-size:12px}} .prose th,.prose td{{padding:.35rem .45rem}} }}
</style>
</head>
<body>

<input type="checkbox" id="theme" class="theme-input" aria-label="Toggle light and dark theme">

<header class="site">
  <a class="wordmark" href="/">S—ML</a>
  <nav aria-label="Sections">
    <a href="/spec/"{spec_cls}>Spec</a><a href="/paper/"{paper_cls}>Paper</a><a href="{doc["md_alt"]}">Raw .md</a><a href="https://github.com/smlweb-org">GitHub</a><label class="theme" for="theme" title="Toggle light / dark"><span aria-hidden="true">◐</span></label>
  </nav>
</header>

<main class="prose">
{body}
</main>

<footer class="site">
  <p class="muted">S—ML Web · CC BY 4.0 · <a href="{doc["md_alt"]}">Download raw Markdown</a> · <a href="https://github.com/smlweb-org">github.com/smlweb-org</a></p>
</footer>

</body>
</html>
"""


def main() -> None:
    for doc in DOCS:
        src = ROOT / doc["src"]
        out = ROOT / doc["out"]
        md = src.read_text(encoding="utf-8")
        body = md_to_html(md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(shell(doc, body), encoding="utf-8")
        size = out.stat().st_size
        print(f"Wrote {doc['out']} ({size:,} bytes)")


if __name__ == "__main__":
    main()
