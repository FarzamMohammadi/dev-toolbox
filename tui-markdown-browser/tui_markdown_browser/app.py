"""Main mdbrowser application."""

import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import DirectoryTree, Footer, Header, Static

from .config import TOC_WIDTHS, WELCOME_MESSAGE
from .messages import ChangeRoot, FileNavigate
from .styles import APP_CSS
from .widgets import MouseOnlyMarkdownViewer, NavDirectoryTree


class MDBrowser(App):
    """Terminal-based markdown file browser with live preview."""

    CSS = APP_CSS

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "reload", "Reload"),
        Binding("t", "toggle_toc", "Toggle TOC"),
        Binding("w", "cycle_toc_width", "TOC Width"),
    ]

    def __init__(self, start_path: str = ".") -> None:
        super().__init__()
        self.start_path = Path(start_path).resolve()
        self.current_file: Path | None = None
        self.toc_width_index = 1  # Start at 15%

    def compose(self) -> ComposeResult:
        """Create the application layout."""
        yield Header()
        yield Vertical(
            MouseOnlyMarkdownViewer(
                WELCOME_MESSAGE,
                show_table_of_contents=True,
                id="preview"
            ),
            Static(f"Path: {self.start_path}", id="path-display"),
            NavDirectoryTree(str(self.start_path), id="files"),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Lock focus to file tree on startup."""
        self.query_one("#files").focus()

    async def load_file(self, path: Path) -> None:
        """Load a file into the preview pane."""
        self.current_file = path
        viewer = self.query_one("#preview", MouseOnlyMarkdownViewer)
        viewer.current_file = path

        # Update path display
        path_display = self.query_one("#path-display", Static)
        path_display.update(f"Path: {path}")

        if path.suffix.lower() == ".md":
            try:
                content = path.read_text(encoding="utf-8")
                await viewer.document.update(content)
            except Exception as e:
                await viewer.document.update(
                    f"# Error\n\nCould not read file:\n```\n{e}\n```"
                )
        else:
            await viewer.document.update(
                f"# Not a Markdown file\n\n"
                f"Selected: `{path.name}`\n\n"
                f"Only `.md` files are rendered. Navigate to a markdown file to preview."
            )

    async def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Handle file selection from tree."""
        await self.load_file(event.path)

    async def on_file_navigate(self, event: FileNavigate) -> None:
        """Handle navigation from clicked links in markdown."""
        # Always sync tree to the file location
        await self.sync_tree_to_file(event.path)

        # Only load/preview if it's a markdown file
        if event.path.suffix.lower() == ".md":
            await self.load_file(event.path)

    async def sync_tree_to_file(self, path: Path) -> None:
        """Sync the file tree to show and select the given file."""
        tree = self.query_one("#files", NavDirectoryTree)
        tree_root = Path(tree.path).resolve()

        # If file is outside current tree root, change root to file's parent
        try:
            path.relative_to(tree_root)
        except ValueError:
            # File is outside tree root - change root to file's parent
            self.start_path = path.parent
            tree.path = str(path.parent)
            tree.reload()

        # Find and select the file node after tree updates
        self.call_later(self._select_file_in_tree, path)

    def _select_file_in_tree(self, path: Path) -> None:
        """Find and select a file node in the tree."""
        tree = self.query_one("#files", NavDirectoryTree)

        def find_node(node, target: Path):
            """Recursively find node matching target path."""
            if node.data and hasattr(node.data, 'path') and node.data.path == target:
                return node
            if node.is_expanded:
                for child in node.children:
                    result = find_node(child, target)
                    if result:
                        return result
            return None

        # Expand path to file first
        tree_root = Path(tree.path).resolve()
        try:
            rel_parts = path.relative_to(tree_root).parts
        except ValueError:
            return

        # Walk and expand each directory in the path
        current = tree.root
        for part in rel_parts[:-1]:  # All but the filename
            if not current.is_expanded:
                current.expand()
            for child in current.children:
                if child.data and hasattr(child.data, 'path') and child.data.path.name == part:
                    current = child
                    break

        # Expand the parent dir if needed
        if not current.is_expanded:
            current.expand()

        # Find and select the file
        target_node = find_node(tree.root, path)
        if target_node:
            tree.select_node(target_node)

    async def on_change_root(self, event: ChangeRoot) -> None:
        """Handle request to change tree root (navigate above current root)."""
        self.start_path = event.path

        # Update path display
        path_display = self.query_one("#path-display", Static)
        path_display.update(f"Path: {event.path}")

        # Replace tree with new root
        tree = self.query_one("#files", NavDirectoryTree)
        tree.path = str(event.path)
        tree.reload()

    def action_reload(self) -> None:
        """Reload the directory tree."""
        tree = self.query_one("#files", DirectoryTree)
        tree.reload()

    def action_toggle_toc(self) -> None:
        """Toggle table of contents visibility."""
        viewer = self.query_one("#preview", MouseOnlyMarkdownViewer)
        viewer.show_table_of_contents = not viewer.show_table_of_contents

    def action_cycle_toc_width(self) -> None:
        """Cycle through TOC width presets."""
        self.toc_width_index = (self.toc_width_index + 1) % len(TOC_WIDTHS)
        width = TOC_WIDTHS[self.toc_width_index]
        viewer = self.query_one("#preview", MouseOnlyMarkdownViewer)
        toc = viewer.query_one("MarkdownTableOfContents")
        if width == 0:
            toc.display = False
        else:
            toc.display = True
            toc.styles.width = f"{width}%"


def main() -> None:
    """CLI entry point."""
    start_path = sys.argv[1] if len(sys.argv) > 1 else "."

    if not Path(start_path).exists():
        print(f"Error: Path '{start_path}' does not exist")
        sys.exit(1)

    app = MDBrowser(start_path)
    app.run()


if __name__ == "__main__":
    main()
