#!/usr/bin/env node

import { readFileSync, writeFileSync } from "fs";
import { basename, dirname, join, extname } from "path";
import { Marked } from "marked";

const inputPath = process.argv[2];
if (!inputPath) {
  console.error("Usage: node convert.js <file.md>");
  process.exit(1);
}

const rawMd = readFileSync(inputPath, "utf-8");

// Pre-process markdown for compatibility
const md = rawMd
  // Strip standalone <br> tags that disrupt block-level parsing
  .replace(/\s*<br\s*\/?>\s*$/gm, "\n")
  // Strip Hashnode-style align attributes from image URLs: ![alt](url align="center") → ![alt](url)
  .replace(/(\!\[[^\]]*\]\([^\s)]+)\s+align="[^"]*"\)/g, "$1)");

// Custom renderer for Medium-optimized HTML
const renderer = {
  heading({ tokens, depth }) {
    const text = this.parser.parseInline(tokens);
    const tag = depth === 1 ? "h1" : depth === 2 ? "h2" : "h3";
    // Medium only supports H1 (title), H2 (large), H3 (small) — collapse H4+ to H3
    return `<${tag}>${text}</${tag}>\n`;
  },

  paragraph({ tokens }) {
    const text = this.parser.parseInline(tokens);
    // If paragraph contains only a <figure>, don't wrap in <p>
    if (/^<figure>.*<\/figure>\s*$/s.test(text)) {
      return text + "\n";
    }
    return `<p>${text}</p>\n`;
  },

  blockquote({ tokens }) {
    const body = this.parser.parse(tokens);
    return `<blockquote>${body}</blockquote>\n`;
  },

  list({ ordered, items }) {
    const tag = ordered ? "ol" : "ul";
    const itemsHtml = items.map((item) => this.listitem(item)).join("\n");
    return `<${tag}>\n${itemsHtml}\n</${tag}>\n`;
  },

  listitem({ tokens }) {
    // Flatten nested lists — Medium doesn't support nesting
    let text = "";
    let nestedHtml = "";
    for (const token of tokens) {
      if (token.type === "list") {
        // Flatten: render nested list items at same level
        for (const item of token.items) {
          nestedHtml += "\n" + this.listitem(item);
        }
      } else if (token.type === "text" && token.tokens) {
        text += this.parser.parseInline(token.tokens);
      } else if (token.type === "space") {
        // skip whitespace tokens
      } else {
        // Block-level tokens (paragraph, code, blockquote, etc.)
        text += this.parser.parse([token]);
      }
    }
    return `<li>${text}</li>${nestedHtml}`;
  },

  code({ text }) {
    // Medium renders <pre> as code blocks (monospace, grey background)
    return `<pre><code>${escapeHtml(text)}</code></pre>\n`;
  },

  codespan({ text }) {
    return `<code>${escapeHtml(text)}</code>`;
  },

  hr() {
    return `<hr>\n`;
  },

  link({ href, title, tokens }) {
    const text = this.parser.parseInline(tokens);
    const titleAttr = title ? ` title="${escapeHtml(title)}"` : "";
    return `<a href="${href}"${titleAttr}>${text}</a>`;
  },

  image({ href, text }) {
    const captionHtml = text
      ? `<figcaption>${escapeHtml(text)}</figcaption>`
      : "";
    return `<figure><img src="${href}" alt="${escapeHtml(text || "")}">${captionHtml}</figure>\n`;
  },

  strong({ tokens }) {
    return `<strong>${this.parser.parseInline(tokens)}</strong>`;
  },

  em({ tokens }) {
    return `<em>${this.parser.parseInline(tokens)}</em>`;
  },

  del({ tokens }) {
    // Medium doesn't support strikethrough — just render the text
    return this.parser.parseInline(tokens);
  },

  br() {
    return `<br>`;
  },

  table({ header, rows }) {
    // Medium has no table support — convert to readable plain text
    let out = `<pre><code>`;
    const allRows = [header, ...rows];

    // Calculate column widths
    const colWidths = header.map((cell, i) => {
      return Math.max(
        cellText(cell).length,
        ...rows.map((row) => cellText(row[i]).length)
      );
    });

    for (let r = 0; r < allRows.length; r++) {
      const row = allRows[r];
      const line = row
        .map((cell, i) => cellText(cell).padEnd(colWidths[i]))
        .join("  │  ");
      out += escapeHtml(line) + "\n";
      if (r === 0) {
        out +=
          escapeHtml(colWidths.map((w) => "─".repeat(w)).join("──┼──")) + "\n";
      }
    }

    out += `</code></pre>\n`;
    return out;
  },

  tablerow({ text }) {
    return text;
  },

  tablecell({ tokens }) {
    return this.parser.parseInline(tokens);
  },
};

function cellText(cell) {
  // Extract plain text from a table cell for width calculation
  if (!cell) return "";
  if (cell.text) return cell.text;
  if (cell.tokens) {
    return cell.tokens.map((t) => t.raw || t.text || "").join("");
  }
  return String(cell);
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// Configure marked
const marked = new Marked({ renderer, gfm: true, breaks: false });

const bodyHtml = marked.parse(md);

// Wrap in full HTML document with Medium-like preview styling
const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${escapeHtml(basename(inputPath, extname(inputPath)))}</title>
<style>
  /* Medium-like preview styling — only for visual preview, does not affect paste */
  body {
    max-width: 680px;
    margin: 40px auto;
    padding: 0 20px;
    font-family: Georgia, Cambria, "Times New Roman", Times, serif;
    font-size: 21px;
    line-height: 1.58;
    color: rgba(0, 0, 0, 0.84);
    background: #fff;
  }
  h1 {
    font-family: "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Geneva, Arial, sans-serif;
    font-size: 40px;
    line-height: 1.15;
    letter-spacing: -0.015em;
    margin-top: 0;
  }
  h2 {
    font-family: "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Geneva, Arial, sans-serif;
    font-size: 30px;
    line-height: 1.22;
    letter-spacing: -0.012em;
    margin-top: 40px;
  }
  h3 {
    font-family: "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Geneva, Arial, sans-serif;
    font-size: 24px;
    line-height: 1.3;
    margin-top: 30px;
  }
  p { margin: 0 0 20px; }
  a { color: inherit; text-decoration: underline; }
  blockquote {
    border-left: 3px solid rgba(0, 0, 0, 0.84);
    margin: 30px 0;
    padding: 0 0 0 20px;
    font-style: italic;
    color: rgba(0, 0, 0, 0.68);
  }
  pre {
    background: rgba(0, 0, 0, 0.05);
    padding: 20px;
    overflow-x: auto;
    border-radius: 3px;
    margin: 30px 0;
  }
  pre code {
    font-family: Menlo, Monaco, "Courier New", Courier, monospace;
    font-size: 16px;
    line-height: 1.5;
    background: none;
    padding: 0;
  }
  code {
    font-family: Menlo, Monaco, "Courier New", Courier, monospace;
    font-size: 18px;
    background: rgba(0, 0, 0, 0.05);
    padding: 2px 5px;
    border-radius: 3px;
  }
  ul, ol { margin: 20px 0; padding-left: 30px; }
  li { margin-bottom: 8px; }
  hr {
    border: none;
    text-align: center;
    margin: 40px 0;
  }
  hr::before {
    content: "...";
    font-size: 30px;
    letter-spacing: 0.6em;
    color: rgba(0, 0, 0, 0.68);
  }
  figure {
    margin: 30px 0;
    text-align: center;
  }
  figure img { max-width: 100%; height: auto; }
  figcaption {
    font-size: 16px;
    color: rgba(0, 0, 0, 0.54);
    margin-top: 10px;
  }
</style>
</head>
<body>
${bodyHtml}
</body>
</html>`;

// Write output alongside input
const outPath = join(dirname(inputPath), basename(inputPath, extname(inputPath)) + ".html");
writeFileSync(outPath, html, "utf-8");
console.log(`✓ Generated: ${outPath}`);
