"""Custom Textual messages for mdbrowser."""

from pathlib import Path

from textual.message import Message


class FileNavigate(Message):
    """Message to request navigation to a file from link click."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__()


class ChangeRoot(Message):
    """Message to request changing the tree root directory."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__()
