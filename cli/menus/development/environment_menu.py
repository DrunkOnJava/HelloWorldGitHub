"""Environment menu implementation."""

from ...models.menu_item import MenuItem

def show_environment_submenu(ui) -> None:
    """Environment variables management submenu."""
    while True:
        ui.print_header(
            "Environment Variables",
            "Manage Environment Configuration"
        )

        menu_items = [
            MenuItem(
                key='view',
                label='View Variables',
                description='View current environment variables',
                icon='👁️',
                shortcut='v'
            ),
            MenuItem(
                key='edit',
                label='Edit Variables',
                description='Edit environment variables',
                icon='✏️',
                shortcut='e'
            ),
            MenuItem(
                key='add',
                label='Add Variable',
                description='Add new environment variable',
                icon='➕',
                shortcut='a'
            ),
            MenuItem(
                key='delete',
                label='Delete Variable',
                description='Remove environment variable',
                icon='🗑️',
                shortcut='d'
            ),
            MenuItem(
                key='validate',
                label='Validate',
                description='Validate environment configuration',
                icon='✓',
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
        elif choice == 'view':
            view_environment_variables(ui)
        elif choice == 'edit':
            edit_environment_variable(ui)
        elif choice == 'add':
            add_environment_variable(ui)
        elif choice == 'delete':
            delete_environment_variable(ui)
        elif choice == 'validate':
            validate_environment_config(ui)

def view_environment_variables(ui) -> None:
    """View current environment variables."""
    env_vars = ui.project.get_environment_variables()
    if not env_vars:
        ui.status_bar.update("No environment variables found", 3)
        return

    print("\nCurrent Environment Variables:")
    for key, value in env_vars.items():
        masked_value = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else value
        print(f"{key}: {masked_value}")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()

def edit_environment_variable(ui) -> None:
    """Edit an existing environment variable."""
    env_vars = ui.project.get_environment_variables()
    if not env_vars:
        ui.status_bar.update("No environment variables found", 3)
        return

    print("\nSelect variable to edit:")
    keys = list(env_vars.keys())
    for i, key in enumerate(keys, 1):
        print(f"{i}. {key}")

    try:
        selection = int(ui.get_input("\nVariable number", required=True)) - 1
        if selection < 0 or selection >= len(keys):
            ui.status_bar.update("Invalid selection", 3)
            return

        key = keys[selection]
        value = ui.get_input(f"New value for {key}", required=True)

        if ui.project.update_environment_variable(key, value):
            ui.status_bar.update(f"Updated {key} successfully", 3)
        else:
            ui.status_bar.update(f"Failed to update {key}", 3)
    except ValueError:
        ui.status_bar.update("Invalid input", 3)

def add_environment_variable(ui) -> None:
    """Add a new environment variable."""
    try:
        key = ui.get_input("Variable name", required=True)
        value = ui.get_input("Variable value", required=True)

        if ui.project.add_environment_variable(key, value):
            ui.status_bar.update(f"Added {key} successfully", 3)
        else:
            ui.status_bar.update(f"Failed to add {key}", 3)
    except Exception as e:
        ui.status_bar.update(f"Error adding variable: {str(e)}", 3)

def delete_environment_variable(ui) -> None:
    """Delete an environment variable."""
    env_vars = ui.project.get_environment_variables()
    if not env_vars:
        ui.status_bar.update("No environment variables found", 3)
        return

    print("\nSelect variable to delete:")
    keys = list(env_vars.keys())
    for i, key in enumerate(keys, 1):
        print(f"{i}. {key}")

    try:
        selection = int(ui.get_input("\nVariable number", required=True)) - 1
        if selection < 0 or selection >= len(keys):
            ui.status_bar.update("Invalid selection", 3)
            return

        key = keys[selection]
        confirm = ui.get_input(f"Are you sure you want to delete {key}? (y/n)").lower()
        if confirm == 'y':
            if ui.project.delete_environment_variable(key):
                ui.status_bar.update(f"Deleted {key} successfully", 3)
            else:
                ui.status_bar.update(f"Failed to delete {key}", 3)
    except ValueError:
        ui.status_bar.update("Invalid input", 3)

def validate_environment_config(ui) -> None:
    """Validate environment configuration."""
    issues = ui.project.validate_environment_config()
    if not issues:
        ui.status_bar.update("Environment configuration is valid", 3)
        return

    print("\nEnvironment Configuration Issues:")
    for issue in issues:
        print(f"- {issue}")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()
