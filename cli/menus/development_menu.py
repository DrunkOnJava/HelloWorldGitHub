"""Development menu implementation."""

from ..models.menu_item import MenuItem

def show_development_menu(ui, project_manager) -> None:
    """Show development tools menu."""
    while True:
        ui.print_header(
            "Development Tools",
            "Run development server, build, and preview"
        )

        menu_items = [
            MenuItem(
                key="server",
                label="Development Server",
                description="Start the development server",
                icon="🚀",
                shortcut="s",
                callback=lambda: project_manager.npm_manager.run_npm_command('dev')
            ),
            MenuItem(
                key="build",
                label="Build Project",
                description="Build the project for production",
                icon="🔨",
                shortcut="b",
                callback=lambda: project_manager.npm_manager.run_npm_command('build')
            ),
            MenuItem(
                key="preview",
                label="Preview Build",
                description="Preview the production build",
                icon="👁️",
                shortcut="p",
                callback=lambda: project_manager.npm_manager.run_npm_command('preview')
            ),
            MenuItem(
                key="watch",
                label="Watch Mode",
                description="Start development server with watch mode",
                icon="👀",
                shortcut="w",
                callback=lambda: project_manager.npm_manager.run_npm_command('watch:css')
            ),
            MenuItem(
                key="back",
                label="Back",
                description="Return to main menu",
                callback=lambda: True
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        selected_item = next((item for item in menu_items if item.key == choice), None)

        if choice == "back" or (selected_item and selected_item.callback()):
            break
