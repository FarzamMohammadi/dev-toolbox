# Medium Post Converter

Converts Markdown blog posts to Medium-optimized HTML for copy-paste publishing. Medium killed their public API, so this is the most reliable way to publish formatted posts.

## Quick Start

```bash
# Install dependencies
npm install

# Convert a markdown file
node convert.js path/to/blog-post.md
```

This generates a `.html` file alongside the input, styled to preview like Medium.

## Usage

```bash
# Convert and open in browser
node convert.js my-post.md
open my-post.html

# Then: Cmd+A → Cmd+C → Medium New Story → Cmd+V
```

## Features

- Medium-optimized HTML output (headings, bold, italic, code blocks, blockquotes, links, images, dividers)
- Nested lists flattened to single level (Medium limitation)
- Tables converted to readable plain-text layout (Medium has no table support)
- Hashnode-style image attributes stripped automatically
- Standalone `<br>` tags cleaned up for proper block parsing
- Medium-like CSS preview styling in output HTML

## Requirements

- Node.js
