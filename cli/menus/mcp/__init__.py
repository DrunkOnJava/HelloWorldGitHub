"""MCP tools menu implementation."""

from ...models.menu_item import MenuItem

def show_mcp_menu(ui) -> None:
    """MCP tools menu implementation with submenus."""
    while True:
        ui.print_header(
            "MCP Tools",
            "Integrated MCP Utilities"
        )

        menu_items = [
            MenuItem(
                key='code_quality',
                label='Code Quality',
                description='Linting, formatting, and code analysis',
                icon='✨',
                shortcut='c'
            ),
            MenuItem(
                key='optimization',
                label='Optimization',
                description='Performance and optimization tools',
                icon='⚡',
                shortcut='o'
            ),
            MenuItem(
                key='project_tools',
                label='Project Tools',
                description='Project management and utilities',
                icon='🛠️',
                shortcut='p'
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
        elif choice == 'code_quality':
            from .code_quality_menu import show_code_quality_submenu
            show_code_quality_submenu(ui)
        elif choice == 'optimization':
            from .optimization_menu import show_optimization_submenu
            show_optimization_submenu(ui)
        elif choice == 'project_tools':
            from .project_tools_menu import show_project_tools_submenu
            show_project_tools_submenu(ui)
