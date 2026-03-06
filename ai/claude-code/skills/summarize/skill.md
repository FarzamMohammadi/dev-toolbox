---
name: summarize
description: Distill files, URLs, and videos into thorough summaries that preserve every valuable detail. Use when user wants to summarize, digest, or extract key points from any source.
allowed-tools: Read, Bash, WebFetch, WebSearch
argument-hint: <file-path-or-url>
---

# Summarize

Distill content to its essence. Preserve every valuable detail. Eliminate only true fluff.

**This is NOT "make it short." This is "extract all value, lose nothing important."**

---

## Step 1: Detect Input Type

Classify the argument:

| Pattern | Type | Method |
|---------|------|--------|
| `youtube.com` or `youtu.be` URL | Video | WebFetch the page for transcript/description. If thin, WebSearch for `"[video title]" transcript` |
| `http://` or `https://` URL | Web | WebFetch the URL. If content is thin (< 200 words), WebSearch for the page title to find a fuller source |
| File path | Local file | Read the file. Use `file [path]` to detect binary vs text if extension is ambiguous |

If no argument provided, ask the user what to summarize.

---

## Step 2: Ingest Fully

Read the ENTIRE source. Do not skim. Do not sample.

- **Long files:** Read all sections. Do not skip middle content.
- **Web pages:** If paginated or truncated, fetch remaining pages.
- **Videos:** Get the full transcript. Partial transcripts produce partial summaries.
- **PDFs:** Use Read with page ranges. Process all pages.

After ingestion, note:
- Total length (word count or duration)
- Structure (sections, chapters, segments)
- Content type (tutorial, argument, narrative, reference, discussion, announcement)

---

## Step 3: Deep Comprehension

Before writing anything, build a mental model:

1. **Central thesis or purpose** — What is this content fundamentally about?
2. **Structural skeleton** — How is the argument or narrative organized?
3. **Key claims and evidence** — What does the author assert and what supports it?
4. **Relationships between ideas** — What depends on what? What contrasts with what?
5. **Unique contributions** — What here is novel, surprising, or non-obvious?

---

## Step 4: Extract All Value

Systematically capture every category of value present:

- **Core arguments and conclusions**
- **Supporting evidence** — data, statistics, research citations
- **Concrete examples** — specific cases, stories, demonstrations
- **Techniques, methods, steps** — actionable how-to content
- **Definitions and mental models** — new vocabulary or frameworks introduced
- **Warnings, caveats, edge cases** — "watch out for X" content
- **Quotes that carry meaning** — preserve phrasing when the exact words matter
- **Code snippets** — preserve any code that demonstrates a concept
- **Links and references** — notable external resources mentioned

---

## Step 5: Eliminate Only True Fluff

Remove ONLY these:
- Filler phrases ("basically," "you know," "so yeah")
- Redundant re-explanations of the same point
- Promotional/self-referential content ("subscribe," "like and share," "in my last post")
- Padding transitions that add no meaning
- Throat-clearing introductions ("In this article, we will discuss...")

**Do NOT cut:**
- Context that aids understanding
- Examples that illuminate abstract points
- Nuances and qualifications
- Author's reasoning process when it reveals how to think about the topic
- Counterarguments or minority opinions presented

---

## Step 6: Compose the Summary

Use the output format below. Adapt section depth to content — a 500-word blog needs fewer sections than a 2-hour lecture.

---

## Step 7: Density Check

Before delivering, verify:

- Could someone who reads ONLY this summary make the same decisions or take the same actions as someone who consumed the original?
- Are all specific numbers, names, and data points preserved?
- Are relationships between ideas clear (not just a flat list of points)?
- Did any section of the original get zero representation? If so, was it truly pure fluff?

If any check fails, go back and fill the gap.

---

## Output Format

```
## Summary: [Title or filename]

**Source:** [file path or URL]
**Type:** [article / tutorial / video / documentation / paper / discussion]
**Length:** [original word count or duration] -> [summary word count] ([X]% density)

---

### Core Message

[2-4 sentences capturing the fundamental thesis, purpose, or takeaway. This is the "if you read nothing else" paragraph.]

---

### Key Points

[Organized by the source's own structure. Use subheadings that reflect the original's organization. Each point gets enough context to stand alone.]

#### [Section/Topic 1]

- [Key point with sufficient context]
- [Supporting detail, data, or example]

#### [Section/Topic 2]

- [Key point]
- [Key point]

[Continue for all major sections]

---

### Specifics Worth Preserving

[Numbers, quotes, code, references, and concrete details that would be lost in a generic summary. Omit this section if the source lacks such specifics.]

- **[Category]:** [specific detail]
- **[Category]:** [specific detail]

---

### Actionable Takeaways

[If the content suggests actions, decisions, or next steps. Omit for purely informational content.]

1. [Specific action or decision point]
2. [Specific action or decision point]
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| Binary/unsupported file (image, compiled) | Report: "Cannot summarize binary file [path]. Supported: text, markdown, code, PDF." |
| Empty file or 404 URL | Report: "Source is empty or unreachable. Verify the path/URL." |
| Very short source (< 100 words) | Summarize anyway, note: "Source is brief ([N] words). Summary preserves full content." |
| Very long source (> 10,000 words) | Proceed fully — thoroughness is the point. Use Step 3 comprehension to organize. |
| Paywalled or login-required URL | Report what was accessible. Suggest: "Content appears paywalled. Provide the text directly or try a cached version." |
| Non-English content | Summarize in the same language as the source, unless user requests otherwise. |
| Code files | Focus on: purpose, architecture, key functions, algorithms, dependencies, notable patterns. |
