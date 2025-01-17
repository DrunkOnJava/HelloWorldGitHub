"""Data models for CLI menu items."""

from dataclasses import dataclass
from typing import Callable, Optional

@dataclass
class MenuItem:
    """Data class for menu items with extended properties."""
    key: str
    label: str
    description: str = ""
    shortcut: str = ""
    disabled: bool = False
    requires_confirmation: bool = False
    icon: str = "○"
    callback: Optional[Callable] = None
