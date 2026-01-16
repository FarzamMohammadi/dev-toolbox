"""File tree widget with custom navigation."""

from pathlib import Path

from textual.binding import Binding
from textual.widgets import DirectoryTree

from ..config import FILTERED_NAMES
from ..messages import ChangeRoot


class NavDirectoryTree(DirectoryTree):
    """
    DirectoryTree with custom navigation:
    - Up/Down: move between items
    - Left: go to parent (cd ..)
    - Right: enter directory
    - Enter: select file for preview
    """

    BINDINGS = [
        Binding("up", "cursor_up_wrap", "Up", show=False),
        Binding("down", "cursor_down_wrap", "Down", show=False),
        Binding("left", "go_parent", "Parent", show=False),
        Binding("right", "enter_dir", "Enter Dir", show=False),
        Binding("enter", "select_node", "Select", show=False),
    ]

    def _get_visible_nodes(self) -> list:
        """Get all currently visible nodes in order."""
        visible = []
        def collect(node):
            visible.append(node)
            if node.is_expanded:
                for child in node.children:
                    collect(child)
        collect(self.root)
        return visible

    def action_cursor_up_wrap(self) -> None:
        """Move cursor up, wrap to bottom if at top."""
        visible = self._get_visible_nodes()
        if visible and self.cursor_node == visible[0]:
            # At top - wrap to bottom
            self.cursor_line = len(visible) - 1
        else:
            # Normal up
            self.action_cursor_up()

    def action_cursor_down_wrap(self) -> None:
        """Move cursor down, wrap to top if at bottom."""
        visible = self._get_visible_nodes()
        if visible and self.cursor_node == visible[-1]:
            # At bottom - wrap to top
            self.cursor_line = 0
        else:
            # Normal down
            self.action_cursor_down()

    def filter_paths(self, paths: list[Path]) -> list[Path]:
        """Filter out hidden files and common noise directories."""
        return [
            p for p in paths
            if not p.name.startswith(".")
            and p.name not in FILTERED_NAMES
        ]

    def action_go_parent(self) -> None:
        """Go to parent directory (cd ..)"""
        node = self.cursor_node
        if node and node.parent:
            # Normal case - go to parent node in tree
            self.select_node(node.parent)
            node.parent.collapse()
        elif node and node.parent is None:
            # At root node - request root change to parent directory
            current_root = Path(self.path).resolve()
            parent_root = current_root.parent
            if parent_root != current_root:  # Not at filesystem root
                self.post_message(ChangeRoot(parent_root))

    def action_enter_dir(self) -> None:
        """Enter directory, or preview .md file."""
        node = self.cursor_node
        if node and node.data:
            path = node.data.path
            if path.is_dir():
                node.expand()
                if node.children:
                    self.select_node(node.children[0])
            elif path.suffix.lower() == ".md":
                # Right arrow on .md file = preview it
                self.post_message(self.FileSelected(node, path))

    def action_select_node(self) -> None:
        """Select current node - triggers file preview."""
        node = self.cursor_node
        if node and node.data:
            path = node.data.path
            if path.is_file():
                self.post_message(self.FileSelected(node, path))
            elif path.is_dir():
                self.action_enter_dir()
