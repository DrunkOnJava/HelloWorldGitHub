"""Assets menu implementation."""

from ...models.menu_item import MenuItem

def show_assets_submenu(ui) -> None:
    """Asset management submenu."""
    while True:
        ui.print_header(
            "Asset Management",
            "CSS and Static Assets"
        )

        menu_items = [
            MenuItem(
                key='css',
                label='Build CSS',
                description='Build Tailwind CSS for production',
                icon='🎨',
                shortcut='c'
            ),
            MenuItem(
                key='css_watch',
                label='Watch CSS',
                description='Watch and rebuild Tailwind CSS on changes',
                icon='👁️',
                shortcut='w'
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
        elif choice == 'css':
            ui.project.run_npm_command('build:css')
        elif choice == 'css_watch':
            ui.project.run_npm_command('watch:css')
