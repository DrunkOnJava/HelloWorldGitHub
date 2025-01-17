"""Code quality tools submenu implementation."""

from ...models.menu_item import MenuItem

def show_code_quality_submenu(ui) -> None:
    """Code quality tools submenu."""
    while True:
        ui.print_header(
            "Code Quality Tools",
            "Linting and Code Analysis"
        )

        menu_items = [
            MenuItem(
                key='eslint',
                label='ESLint Tools',
                description='ESLint checking and fixing',
                icon='🔧',
                shortcut='e'
            ),
            MenuItem(
                key='typescript',
                label='TypeScript Tools',
                description='TypeScript validation and fixes',
                icon='📝',
                shortcut='t'
            ),
            MenuItem(
                key='analyze',
                label='Code Analysis',
                description='Code quality analysis',
                icon='🔍',
                shortcut='a'
            ),
            MenuItem(
                key='back',
                label='Back to MCP Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'eslint':
            from .eslint_menu import show_eslint_submenu
            show_eslint_submenu(ui)
        elif choice == 'typescript':
            from .typescript_menu import show_typescript_submenu
            show_typescript_submenu(ui)
        elif choice == 'analyze':
            from .analysis_menu import show_analysis_submenu
            show_analysis_submenu(ui)
