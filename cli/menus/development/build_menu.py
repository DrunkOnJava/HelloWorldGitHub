"""Build menu implementation."""

from ...models.menu_item import MenuItem

def show_build_submenu(ui) -> None:
    """Build options submenu."""
    while True:
        ui.print_header(
            "Build Options",
            "Project Build Management"
        )

        menu_items = [
            MenuItem(
                key='build',
                label='Production Build',
                description='Build project with Astro and Tailwind CSS for production',
                icon='🏗️',
                shortcut='b'
            ),
            MenuItem(
                key='clean',
                label='Clean Build',
                description='Clean build artifacts and reinstall dependencies',
                icon='🧹',
                shortcut='c'
            ),
            MenuItem(
                key='back',
                label='Back to Development Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'build':
            ui.project.run_npm_command('build')
        elif choice == 'clean':
            ui.project.run_npm_command('clean')
