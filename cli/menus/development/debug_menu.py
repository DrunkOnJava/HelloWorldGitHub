"""Debug menu implementation."""

from ...models.menu_item import MenuItem

def show_debug_submenu(ui) -> None:
    """Debug tools submenu."""
    while True:
        ui.print_header(
            "Debug Tools",
            "Debugging and Troubleshooting"
        )

        menu_items = [
            MenuItem(
                key='config',
                label='Configure Debugger',
                description='Configure debugger settings',
                icon='⚙️',
                shortcut='c'
            ),
            MenuItem(
                key='breakpoints',
                label='Breakpoints',
                description='Manage breakpoints',
                icon='🔍',
                shortcut='b'
            ),
            MenuItem(
                key='inspect',
                label='Inspect Variable',
                description='Inspect variable during debugging',
                icon='👁️',
                shortcut='i'
            ),
            MenuItem(
                key='stack',
                label='Call Stack',
                description='View current call stack',
                icon='📚',
                shortcut='s'
            ),
            MenuItem(
                key='console',
                label='Debug Console',
                description='View debug console output',
                icon='💻',
                shortcut='d'
            ),
            MenuItem(
                key='start',
                label='Start Debug Session',
                description='Start a new debug session',
                icon='▶️',
                shortcut='t'
            ),
            MenuItem(
                key='stop',
                label='Stop Debug Session',
                description='Stop current debug session',
                icon='⏹️',
                shortcut='p'
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
        elif choice == 'config':
            configure_debugger(ui)
        elif choice == 'breakpoints':
            manage_breakpoints(ui)
        elif choice == 'inspect':
            inspect_variable(ui)
        elif choice == 'stack':
            view_call_stack(ui)
        elif choice == 'console':
            view_debug_console(ui)
        elif choice == 'start':
            start_debug_session(ui)
        elif choice == 'stop':
            stop_debug_session(ui)

def configure_debugger(ui) -> None:
    """Configure debugger settings."""
    ui.print_header(
        "Configure Debugger",
        "Debug Configuration Settings"
    )

    config = {
        'sourceMap': ui.get_input("Enable source maps? (y/n)", required=True).lower() == 'y',
        'console': ui.get_input("Enable debug console? (y/n)", required=True).lower() == 'y',
        'breakOnError': ui.get_input("Break on error? (y/n)", required=True).lower() == 'y'
    }

    if ui.project.configure_debugger(config):
        ui.status_bar.update("Debugger configured successfully", 3)
    else:
        ui.status_bar.update("Failed to configure debugger", 3)

def manage_breakpoints(ui) -> None:
    """Manage breakpoints."""
    while True:
        ui.print_header(
            "Breakpoint Management",
            "Manage Debug Breakpoints"
        )

        menu_items = [
            MenuItem(
                key='add',
                label='Add Breakpoint',
                description='Add a new breakpoint',
                icon='➕',
                shortcut='a'
            ),
            MenuItem(
                key='remove',
                label='Remove Breakpoint',
                description='Remove existing breakpoint',
                icon='➖',
                shortcut='r'
            ),
            MenuItem(
                key='list',
                label='List Breakpoints',
                description='Show all breakpoints',
                icon='📋',
                shortcut='l'
            ),
            MenuItem(
                key='back',
                label='Back to Debug Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'add':
            data = {
                'file': ui.get_input("File path", required=True),
                'line': int(ui.get_input("Line number", required=True))
            }
            if ui.project.manage_breakpoints('add', data):
                ui.status_bar.update("Breakpoint added successfully", 3)
            else:
                ui.status_bar.update("Failed to add breakpoint", 3)
        elif choice == 'remove':
            data = {
                'file': ui.get_input("File path", required=True),
                'line': int(ui.get_input("Line number", required=True))
            }
            if ui.project.manage_breakpoints('remove', data):
                ui.status_bar.update("Breakpoint removed successfully", 3)
            else:
                ui.status_bar.update("Failed to remove breakpoint", 3)
        elif choice == 'list':
            if not ui.project.manage_breakpoints('list'):
                ui.status_bar.update("No breakpoints found", 3)

def inspect_variable(ui) -> None:
    """Inspect variable during debugging."""
    variable_name = ui.get_input("Variable name to inspect", required=True)
    result = ui.project.inspect_variable(variable_name)

    if result:
        print("\nVariable Information:")
        for key, value in result.items():
            print(f"{key}: {value}")
        print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
        input()
    else:
        ui.status_bar.update("Failed to inspect variable", 3)

def view_call_stack(ui) -> None:
    """View current call stack."""
    stack = ui.project.get_call_stack()

    if stack:
        print("\nCall Stack:")
        for frame in stack:
            print(f"File: {frame.get('file', 'unknown')}")
            print(f"Line: {frame.get('line', 'unknown')}")
            print(f"Function: {frame.get('function', 'unknown')}\n")
        print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
        input()
    else:
        ui.status_bar.update("No call stack available", 3)

def view_debug_console(ui) -> None:
    """View debug console output."""
    output = ui.project.get_debug_console()

    if output:
        print("\nDebug Console Output:")
        for line in output:
            print(line)
        print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
        input()
    else:
        ui.status_bar.update("No console output available", 3)

def start_debug_session(ui) -> None:
    """Start a debug session."""
    config_name = ui.get_input("Debug configuration name (optional)")
    if ui.project.start_debug_session(config_name):
        ui.status_bar.update("Debug session started successfully", 3)
    else:
        ui.status_bar.update("Failed to start debug session", 3)

def stop_debug_session(ui) -> None:
    """Stop the current debug session."""
    if ui.project.stop_debug_session():
        ui.status_bar.update("Debug session stopped successfully", 3)
    else:
        ui.status_bar.update("Failed to stop debug session", 3)
