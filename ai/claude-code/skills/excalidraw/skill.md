---
name: excalidraw
description: Generate .excalidraw JSON files for architecture flows, system diagrams, and simple sketches from natural-language descriptions. Use whenever the user asks to draw, sketch, diagram, or visualize a flow, architecture, pipeline, or system with a small number of boxes (up to ~15) — especially for slides, docs, or when they mention excalidraw. Also trigger when the user describes components and their connections ("X calls Y which writes to Z") and wants something they can open in excalidraw.com.
allowed-tools: Read, Write, Bash
---

# Excalidraw Diagram Skill

Generate clean `.excalidraw` JSON files that open in excalidraw.com or the Excalidraw desktop app. Best for architecture flows, sequence sketches, and small system diagrams with under ~15 nodes.

## Why this skill exists

Excalidraw's file format is plain JSON, so Claude can produce it directly with `Write` — no server, no renderer, no MCP needed. The parts that warrant a skill are (a) the element shape, (b) correct arrow↔node binding (often done wrong), and (c) choosing a layout that looks clean without fiddling with coordinates.

## Workflow

### 1. Gather
Confirm these quickly if the user hasn't already specified them:
- **Nodes**: the box labels, in order
- **Edges**: which nodes connect, in which direction, and any edge labels
- **Orientation**: left-to-right (LR) or top-to-bottom (TB)
- **Output path**: where to save (default `./diagram.excalidraw`)

Skip the confirmation when the user has given an unambiguous spec (e.g. "3 boxes: User → Alfie → MCP Server, save to /tmp/test.excalidraw"). Don't ask for the sake of asking.

### 2. Plan the layout
Pick a template based on node count and relationships:

| Template | When to use | Node count |
|---|---|---|
| Horizontal LR | Linear flow, default for slides | 3–6 |
| Vertical TB | Tall slides, long chains, many steps | 7–15 |
| Fan-out | One source → multiple targets | 1 source, 2–6 targets |

### 3. Generate the JSON
Use the Format Reference and Arrow Binding sections below, with coordinates from the chosen template. When in doubt, copy the structure from [`examples/user-alfie-mcp.excalidraw`](examples/user-alfie-mcp.excalidraw) and modify — it's a complete working file.

### 4. Output
After writing, tell the user:
- The absolute path of the file
- How to open it: "Open at https://excalidraw.com (drag-drop) or Excalidraw desktop: File → Open"

---

## Format Reference

### Top-level wrapper
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [ /* your elements */ ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

### Common element fields
Every element (rectangle, text, arrow) needs these. Fields marked `*` are the ones Claude most often forgets.

```json
{
  "id": "box-1",
  "type": "rectangle",
  "x": 100, "y": 300,
  "width": 180, "height": 80,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "roundness": { "type": 3 },
  "seed": 1,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1,
  "link": null,
  "locked": false
}
```

`id` must be unique. `seed` and `versionNonce` can be any integers (Excalidraw regenerates them on edit). `roundness: { "type": 3 }` gives boxes soft corners and looks much better than square — use it on all rectangles. Use `null` when the user explicitly wants sharp corners.

### Text inside a box
A label inside a box is a *separate* text element with `containerId` set to the box's id. The box must also list the text in its `boundElements`.

```json
{
  "id": "text-1",
  "type": "text",
  "x": 100, "y": 300,
  "width": 180, "height": 80,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "roundness": null,
  "seed": 2,
  "version": 1,
  "versionNonce": 2,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1,
  "link": null,
  "locked": false,
  "text": "User",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "baseline": 18,
  "containerId": "box-1",
  "originalText": "User",
  "lineHeight": 1.25
}
```

`fontFamily: 1` is the hand-drawn Virgil font — use it as the default for the recognizable Excalidraw look. Use `2` (Helvetica) only when the user wants a clean, non-sketchy style.

### Arrow between two boxes
```json
{
  "id": "arrow-1",
  "type": "arrow",
  "x": 280, "y": 340,
  "width": 80, "height": 0,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "roundness": { "type": 2 },
  "seed": 3,
  "version": 1,
  "versionNonce": 3,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1,
  "link": null,
  "locked": false,
  "points": [[0, 0], [80, 0]],
  "lastCommittedPoint": null,
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "startBinding": { "elementId": "box-1", "focus": 0, "gap": 0 },
  "endBinding":   { "elementId": "box-2", "focus": 0, "gap": 0 },
  "elbowed": false
}
```

`points` are offsets *from the arrow's own `x,y`*. `[[0,0], [80,0]]` means an 80-px horizontal segment starting at the arrow's origin. The arrow's `x,y` sits at the start point in world coordinates. Use `{ "type": 2 }` roundness on arrows for smooth curves at waypoints.

---

## Arrow Binding (the gotcha)

This is what people get wrong. Every arrow connecting two boxes needs **reciprocal bindings**:

1. Arrow's `startBinding.elementId` → source box id
2. Arrow's `endBinding.elementId` → target box id
3. **Both boxes must list the arrow** in their own `boundElements`:
   ```json
   "boundElements": [
     { "id": "text-1", "type": "text" },
     { "id": "arrow-1", "type": "arrow" }
   ]
   ```

Missing the reciprocal bind means the arrow renders but disconnects from the box when moved in the editor, and in some Excalidraw versions it won't render at all. Always set it on both sides.

### `focus` and `gap`
- `focus: 0` = aims at the box's center. `-1` / `1` bias to one edge. `0` is almost always right.
- `gap: 0` = arrow touches the box edge. Increase for visual breathing room.

---

## Layout Templates

Defaults for all templates: `strokeWidth: 2`, `fontSize: 20`, `fontFamily: 1`, boxes `roundness: { "type": 3 }`, arrows `roundness: { "type": 2 }`.

### Horizontal LR — 3–6 nodes
- Box size: `180 × 80`
- Gap between boxes: `80 px`
- All boxes on row `y = 300` (vertical center `y = 340`)
- Box `i` at `x = 100 + 260*i` → positions 100, 360, 620, 880, 1140, 1400
- Arrow from box `i` to `i+1`: `x = 100 + 260*i + 180`, `y = 340`, `width = 80`, `height = 0`, `points = [[0,0], [80,0]]`

### Vertical TB — 7–15 nodes
- Box size: `220 × 70`
- Gap between boxes: `60 px`
- All boxes on column `x = 200` (horizontal center `x = 310`)
- Box `i` at `y = 100 + 130*i`
- Arrow from box `i` to `i+1`: `x = 310`, `y = 100 + 130*i + 70`, `width = 0`, `height = 60`, `points = [[0,0], [0,60]]`

### Fan-out — 1 source → N targets
- Source box: `180 × 80` at `x = 100`
- Target boxes: `180 × 80` at `x = 500`, vertical gap `40 px` (y spacing `120`)
- Targets centered around the source: target `i` at `y = source_center_y - (N-1)*60 + 120*i`, where `source_center_y = source.y + 40`
- Source-box `y` typically 300 for a small group; for N=3 targets place them at y = 200, 320, 440 and source at y = 280 (center = 320)
- Arrow from source right-edge to target left-edge: `x = 280`, `y = source_center_y`, `width = 220`, `height = target_center_y - source_center_y`, `points = [[0,0], [220, target_center_y - source_center_y]]`

---

## Worked Example

[`examples/user-alfie-mcp.excalidraw`](examples/user-alfie-mcp.excalidraw) is a complete 3-box horizontal flow: User → Alfie → MCP Server. Use it as the reference implementation — copy and modify labels/positions for similar flows.

---

## Tips

- **Colors for slides**: black-on-white reads best. `strokeColor: "#1e1e1e"`, `backgroundColor: "transparent"`. Highlight one critical box with `backgroundColor: "#ffec99"` (soft yellow) and `fillStyle: "solid"` if the user wants emphasis.
- **Edge labels**: create a text element with the arrow's id as its `containerId`, and add it to the arrow's `boundElements`. Keep labels to 1–3 words; longer hurts readability.
- **Slide aspect ratio**: horizontal LR with up to 4 boxes fits ~1600 px wide without scroll, which works for 16:9 slides.
- **Editing existing files**: read the file first, modify just the relevant elements, and write back. Don't regenerate from scratch unless the user asks for a full redo — they may have tweaked positions by hand.

## When to recommend something else

If the user wants 20+ nodes, precise alignment, or complex routing (UML, ERDs, detailed schematics), this skill isn't the right tool. Recommend Mermaid (for text-spec diagrams), draw.io (for formal shapes), or the yctimlin excalidraw MCP server (Docker-based, live canvas) if they need heavier-duty work.
