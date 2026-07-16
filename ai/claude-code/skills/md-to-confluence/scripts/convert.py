#!/usr/bin/env python3
"""Markdown -> Confluence storage format (XHTML).

Confluence Cloud stores pages as "storage format", an XHTML dialect. A raw
copy-paste of Markdown source does not render tables, headings, or diagrams,
so we convert first and push the result via the REST API (see publish.py).

Handles N ```mermaid``` blocks: each is extracted to <mmd-dir>/diagram-<i>.mmd
and replaced in the body by an <ac:image> macro referencing an attachment named
mermaid-<i>.png. publish.py renders those .mmd files to PNG and uploads them.

A native Confluence table-of-contents macro is prepended so long docs get a
clickable outline that auto-updates.

Usage: convert.py SRC.md OUT.html MMD_DIR
"""
import re, sys, pathlib
import markdown  # pip install --user --break-system-packages markdown

SRC = pathlib.Path(sys.argv[1])
OUT_HTML = pathlib.Path(sys.argv[2])
MMD_DIR = pathlib.Path(sys.argv[3])
MMD_DIR.mkdir(parents=True, exist_ok=True)

text = SRC.read_text()

# 0. Sanitize the two mermaid-syntax mistakes that abort a whole render but are
#    trivially auto-fixable, and only on sequence-diagram *message* lines
#    (`A->>B: text`) — never on Notes or flowchart node/edge labels, where the
#    same characters are legal:
#      - `<br/>` is a hard parse error on a message line (it's only valid inside
#        a `Note`). We join the line back together with a space.
#      - `;` terminates a statement in mermaid, so it silently truncates a
#        message mid-sentence. We swap it for a comma so the text survives.
#    Both are cosmetic-only fixes to text that could not render otherwise; no
#    word of the visible content is lost.
_ARROW = re.compile(r"-{1,2}(>>?|[x)])")
_MSG_KEYWORDS = (
    "note", "participant", "actor", "loop", "alt", "opt", "else", "end",
    "par", "and", "rect", "activate", "deactivate", "autonumber", "critical",
    "break", "box", "link", "links",
)
_sanitized = 0

def _sanitize_mermaid(block):
    """Fix `<br/>` and `;` on sequence-diagram message lines only."""
    global _sanitized
    lines = block.split("\n")
    first = next((ln.strip() for ln in lines if ln.strip()), "")
    if not first.startswith("sequenceDiagram"):
        return block  # only sequence messages carry these two hazards
    out = []
    for line in lines:
        low = line.lstrip().lower()
        is_msg = (
            _ARROW.search(line) and ":" in line
            and not low.startswith(_MSG_KEYWORDS)
        )
        if is_msg:
            head, sep, msg = line.partition(":")
            fixed = re.sub(r"\s*<br\s*/?>\s*", " ", msg).replace(";", ",")
            if fixed != msg:
                _sanitized += 1
            line = head + sep + fixed
        out.append(line)
    return "\n".join(out)

# 1. Pull every mermaid block out before Markdown conversion (Markdown would
#    otherwise mangle it), leaving a unique token in its place.
blocks = []
def _grab(m):
    idx = len(blocks)
    blocks.append(_sanitize_mermaid(m.group(1)))
    return f"\n\nMERMAIDTOKEN{idx}ENDTOKEN\n\n"

text = re.sub(r"```mermaid\n(.*?)```", _grab, text, flags=re.DOTALL)
for i, b in enumerate(blocks):
    (MMD_DIR / f"diagram-{i}.mmd").write_text(b)

# 2. Convert the rest. `tables` gives real <table>; the others cover fenced
#    code, tight lists, and raw HTML passthrough.
html = markdown.markdown(
    text,
    extensions=["tables", "fenced_code", "sane_lists", "md_in_html"],
)

# 3. Swap each token for a Confluence image macro pointing at its attachment.
for i in range(len(blocks)):
    macro = (
        f'<ac:image ac:align="center" ac:width="800">'
        f'<ri:attachment ri:filename="mermaid-{i}.png" /></ac:image>'
    )
    tok = f"MERMAIDTOKEN{i}ENDTOKEN"
    html = html.replace(f"<p>{tok}</p>", macro).replace(tok, macro)

# 4. Auto table-of-contents (native macro, levels 2-3).
toc = ('<ac:structured-macro ac:name="toc">'
       '<ac:parameter ac:name="minLevel">2</ac:parameter>'
       '<ac:parameter ac:name="maxLevel">3</ac:parameter>'
       '</ac:structured-macro>\n')
html = toc + html

OUT_HTML.write_text(html)
print(f"tables={html.count('<table>')} mermaid_blocks={len(blocks)} "
      f"mermaid_autofixes={_sanitized} chars={len(html)}")
