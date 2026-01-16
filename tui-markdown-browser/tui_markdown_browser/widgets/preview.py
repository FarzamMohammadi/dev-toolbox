"""Markdown preview widget with mouse-only interaction."""

import webbrowser
from pathlib import Path

from textual.widgets import Markdown, MarkdownViewer

from ..messages import FileNavigate


class MouseOnlyMarkdownViewer(MarkdownViewer):
    """MarkdownViewer that only responds to mouse, never takes keyboard focus."""

    can_focus = False
    can_focus_children = False

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_file: Path | None = None

    async def go(self, location: str) -> None:
        """Override go to handle links with proper path resolution."""
        # Anchor links - scroll within document
        if location.startswith("#"):
            self.document.goto_anchor(location[1:])
            return

        # External URLs - open in browser
        if location.startswith(("http://", "https://", "mailto:", "tel:")):
            webbrowser.open(location)
            return

        # Relative file links - resolve from current file's directory
        if self.current_file:
            # Strip anchor if present
            path_part = location.split("#")[0]
            target = (self.current_file.parent / path_part).resolve()

            if target.exists():
                # Navigate to file via our app's handler
                self.post_message(FileNavigate(target))
            else:
                await self.document.update(
                    f"# File Not Found\n\n"
                    f"Could not find: `{location}`\n\n"
                    f"Resolved path: `{target}`"
                )
