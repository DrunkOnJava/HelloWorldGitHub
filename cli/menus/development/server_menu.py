"""Server menu implementation."""

from ...models.menu_item import MenuItem

def show_server_submenu(ui) -> None:
    """Server options submenu."""
    while True:
        ui.print_header(
            "Server Options",
            "Development Server Management"
        )

        menu_items = [
            MenuItem(
                key='dev',
                label='Start Development Server',
                description='Run Astro dev server with hot reloading',
                icon='🔄',
                shortcut='d'
            ),
            MenuItem(
                key='preview',
                label='Preview Build',
                description='Preview production build locally',
                icon='👀',
                shortcut='p'
            ),
            MenuItem(
                key='host',
                label='Host Options',
                description='Configure host and port settings',
                icon='🌐',
                shortcut='h'
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
        elif choice == 'dev':
            ui.project.run_npm_command('dev')
        elif choice == 'preview':
            ui.project.run_npm_command('preview')
        elif choice == 'host':
            configure_host(ui)

def configure_host(ui) -> None:
    """Configure development server host and port."""
    ui.print_header(
        "Host Configuration",
        "Configure Development Server Settings"
    )

    # Get current configuration
    current_config = ui.project.get_host_config()

    print("\nCurrent Configuration:")
    print(f"Host: {current_config['host']}")
    print(f"Port: {current_config['port']}")
    print("\nEnter new values or press Enter to keep current values")

    # Get new configuration
    host = ui.get_input(f"Host [{current_config['host']}]") or current_config['host']

    try:
        port_str = ui.get_input(f"Port [{current_config['port']}]") or str(current_config['port'])
        port = int(port_str)
        if port < 1 or port > 65535:
            raise ValueError("Port must be between 1 and 65535")
    except ValueError as e:
        ui.status_bar.update(f"Invalid port number: {str(e)}", 3)
        return

    # Update configuration
    if ui.project.configure_host(host, port):
        ui.status_bar.update("Host configuration updated successfully", 3)
    else:
        ui.status_bar.update("Failed to update host configuration", 3)
