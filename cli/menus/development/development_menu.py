"""Main development menu implementation."""

from ...models.menu_item import MenuItem
from . import (
    server_menu,
    build_menu,
    environment_menu,
    performance_menu,
    bundle_menu,
    debug_menu,
    code_quality_menu,
    documentation_menu,
    assets_menu
)

def show_development_menu(ui) -> None:
    """Development menu implementation with submenus."""
    while True:
        ui.print_header(
            "Development",
            "Build and Run Options"
        )

        menu_items = [
            MenuItem(
                key='debug',
                label='Debug Tools',
                description='Debugging and troubleshooting tools',
                icon='🔧',
                shortcut='d'
            ),
            MenuItem(
                key='quality',
                label='Code Quality',
                description='Code formatting and style enforcement',
                icon='✨',
                shortcut='q'
            ),
            MenuItem(
                key='server',
                label='Server Options',
                description='Development server and preview options',
                icon='🖥️',
                shortcut='s'
            ),
            MenuItem(
                key='build_options',
                label='Build Options',
                description='Project build and compilation',
                icon='🏗️',
                shortcut='b'
            ),
            MenuItem(
                key='assets',
                label='Asset Management',
                description='CSS, images, and static assets',
                icon='🎨',
                shortcut='a'
            ),
            MenuItem(
                key='env',
                label='Environment',
                description='Manage environment variables',
                icon='🔐',
                shortcut='e'
            ),
            MenuItem(
                key='profile',
                label='Performance',
                description='Performance profiling tools',
                icon='📊',
                shortcut='p'
            ),
            MenuItem(
                key='bundle',
                label='Bundle Analysis',
                description='Analyze and optimize bundles',
                icon='📦',
                shortcut='n'
            ),
            MenuItem(
                key='deps',
                label='Dependencies',
                description='Manage project dependencies',
                icon='📦',
                shortcut='d'
            ),
            MenuItem(
                key='docs',
                label='Documentation',
                description='Documentation tools and generation',
                icon='📚',
                shortcut='o'
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
        elif choice == 'debug':
            debug_menu.show_debug_submenu(ui)
        elif choice == 'quality':
            code_quality_menu.show_code_quality_submenu(ui)
        elif choice == 'server':
            server_menu.show_server_submenu(ui)
        elif choice == 'build_options':
            build_menu.show_build_submenu(ui)
        elif choice == 'assets':
            assets_menu.show_assets_submenu(ui)
        elif choice == 'env':
            environment_menu.show_environment_submenu(ui)
        elif choice == 'profile':
            performance_menu.show_performance_submenu(ui)
        elif choice == 'bundle':
            bundle_menu.show_bundle_submenu(ui)
        elif choice == 'deps':
            documentation_menu.show_dependency_submenu(ui)
        elif choice == 'docs':
            documentation_menu.show_documentation_submenu(ui)
