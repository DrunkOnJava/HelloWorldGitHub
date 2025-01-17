"""Page management menu package."""

from .template_menu import show_template_menu
from .structure_menu import show_structure_menu
from .metadata_menu import show_metadata_menu

__all__ = [
    'show_template_menu',
    'show_structure_menu',
    'show_metadata_menu'
]
