# Architecture Mapper

Tools for understanding and documenting project architecture.

## Templates

Static markdown templates for AI or humans to manually document architecture - user flows, architecture patterns, component diagrams, data flow, etc.

- [`ARCHITECTURE.md`](./ARCHITECTURE.md) - Main architecture documentation template

Copy the template to your project root and fill in the sections as needed.

## Git Visualizer

Generates animated repository history videos using [gource](https://gource.io/), showing how the codebase evolved over time.

```bash
cd git-visualizer
./run.sh  # does everything: checks tools, offers to install, generates video
```

Output is saved to `git-visualizer/output/gource/`.
