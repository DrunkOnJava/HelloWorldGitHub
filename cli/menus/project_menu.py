"""Project-specific tools menu implementation."""

from ..models.menu_item import MenuItem
from .project.compound_menu import show_compound_menu
from .project.component_menu import show_component_menu
from .project.page_menu import show_page_menu

def show_project_menu(ui) -> None:
    """Project-specific tools menu implementation with submenus."""
    while True:
        ui.print_header(
            "Project Tools",
            "Project-Specific Utilities"
        )

        menu_items = [
            MenuItem(
                key='compound',
                label='Compound Manager',
                description='Manage compound data and pages',
                icon='💊',
                shortcut='c'
            ),
            MenuItem(
                key='pages',
                label='Page Management',
                description='Generate and manage pages',
                icon='📄',
                shortcut='p'
            ),
            MenuItem(
                key='components',
                label='Component Tools',
                description='Create and manage components',
                icon='🧩',
                shortcut='m'
            ),
            MenuItem(
                key='back',
                label='Back to Main Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'compound':
            show_compound_menu(ui)
        elif choice == 'pages':
            show_page_menu(ui)
        elif choice == 'components':
            show_component_menu(ui)
