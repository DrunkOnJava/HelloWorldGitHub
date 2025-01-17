"""Template management menu implementation."""

from ....models.menu_item import MenuItem

def show_template_menu(ui) -> None:
    """Template management submenu."""
    while True:
        ui.print_header(
            "Template Management",
            "Manage Page Templates"
        )

        menu_items = [
            MenuItem(
                key='list',
                label='List Templates',
                description='View available templates',
                icon='📋',
                shortcut='l'
            ),
            MenuItem(
                key='create',
                label='Create Template',
                description='Create new page template',
                icon='➕',
                shortcut='c'
            ),
            MenuItem(
                key='edit',
                label='Edit Template',
                description='Modify existing template',
                icon='✏️',
                shortcut='e'
            ),
            MenuItem(
                key='delete',
                label='Delete Template',
                description='Remove template',
                icon='🗑️',
                shortcut='d'
            ),
            MenuItem(
                key='back',
                label='Back to Pages Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'list':
            list_templates(ui)
        elif choice == 'create':
            create_template(ui)
        elif choice == 'edit':
            edit_template(ui)
        elif choice == 'delete':
            delete_template(ui)

def list_templates(ui) -> None:
    """List available page templates."""
    templates = ui.project.get_templates()
    if not templates:
        ui.status_bar.update("No templates found", 2)
        return

    print("\nAvailable Templates:")
    for template in templates:
        print(f"\n{ui.theme.COLORS['HEADER']}{template['name']}{ui.theme.COLORS['ENDC']}")
        print(f"Description: {template['description']}")
        print(f"Path: {template['path']}")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()

def create_template(ui) -> None:
    """Create a new page template."""
    try:
        name = ui.get_input("Template name", required=True)
        description = ui.get_input("Template description", required=True)
        content = ui.get_input("Template content (HTML/Astro)", required=True)

        if ui.project.create_template(name, description, content):
            ui.status_bar.update(f"Template '{name}' created successfully", 2)
        else:
            ui.status_bar.update("Failed to create template", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error creating template: {str(e)}", 2, error=True)

def edit_template(ui) -> None:
    """Edit an existing template."""
    templates = ui.project.get_templates()
    if not templates:
        ui.status_bar.update("No templates found", 2)
        return

    print("\nSelect template to edit:")
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template['name']}")

    try:
        selection = int(ui.get_input("\nTemplate number", required=True)) - 1
        if selection < 0 or selection >= len(templates):
            ui.status_bar.update("Invalid selection", 2, error=True)
            return

        template = templates[selection]
        print(f"\nEditing template: {template['name']}")
        print("Press Enter to keep current values")

        name = ui.get_input(f"Name [{template['name']}]") or template['name']
        description = ui.get_input(f"Description [{template['description']}]") or template['description']
        content = ui.get_input(f"Content (current content will be shown in editor)") or template['content']

        if ui.project.update_template(template['name'], name, description, content):
            ui.status_bar.update(f"Template '{name}' updated successfully", 2)
        else:
            ui.status_bar.update("Failed to update template", 2, error=True)
    except ValueError:
        ui.status_bar.update("Invalid input", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error updating template: {str(e)}", 2, error=True)

def delete_template(ui) -> None:
    """Delete an existing template."""
    templates = ui.project.get_templates()
    if not templates:
        ui.status_bar.update("No templates found", 2)
        return

    print("\nSelect template to delete:")
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template['name']}")

    try:
        selection = int(ui.get_input("\nTemplate number", required=True)) - 1
        if selection < 0 or selection >= len(templates):
            ui.status_bar.update("Invalid selection", 2, error=True)
            return

        template = templates[selection]
        confirm = ui.get_input(f"Are you sure you want to delete '{template['name']}'? (y/n)").lower()
        if confirm == 'y':
            if ui.project.delete_template(template['name']):
                ui.status_bar.update(f"Template '{template['name']}' deleted successfully", 2)
            else:
                ui.status_bar.update("Failed to delete template", 2, error=True)
    except ValueError:
        ui.status_bar.update("Invalid input", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error deleting template: {str(e)}", 2, error=True)
