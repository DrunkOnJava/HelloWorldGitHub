"""Page management menu implementation."""

from ...models.menu_item import MenuItem
from .page import show_template_menu, show_structure_menu, show_metadata_menu

def show_page_menu(ui) -> None:
    """Page management submenu."""
    while True:
        ui.print_header(
            "Page Management",
            "Generate and Manage Pages"
        )

        menu_items = [
            MenuItem(
                key='create',
                label='Create Page',
                description='Create new page from template',
                icon='📄',
                shortcut='c'
            ),
            MenuItem(
                key='templates',
                label='Manage Templates',
                description='Edit page templates',
                icon='📋',
                shortcut='t'
            ),
            MenuItem(
                key='structure',
                label='Page Structure',
                description='Manage page hierarchy',
                icon='🗂️',
                shortcut='s'
            ),
            MenuItem(
                key='metadata',
                label='Metadata',
                description='Manage page metadata',
                icon='🏷️',
                shortcut='m'
            ),
            MenuItem(
                key='back',
                label='Back to Project Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'create':
            create_page(ui)
        elif choice == 'templates':
            show_template_menu(ui)
        elif choice == 'structure':
            show_structure_menu(ui)
        elif choice == 'metadata':
            show_metadata_menu(ui)

def create_page(ui) -> None:
    """Create a new page from template."""
    templates = ui.project.get_templates()
    if not templates:
        ui.status_bar.update("No templates available. Please create a template first.", 2)
        return

    try:
        print("\nSelect template:")
        for i, template in enumerate(templates, 1):
            print(f"{i}. {template['name']} - {template['description']}")

        selection = int(ui.get_input("\nTemplate number", required=True)) - 1
        if selection < 0 or selection >= len(templates):
            ui.status_bar.update("Invalid selection", 2, error=True)
            return

        template = templates[selection]
        path = ui.get_input("Page path (e.g., guides/getting-started)", required=True)
        title = ui.get_input("Page title", required=True)
        description = ui.get_input("Page description", required=True)

        metadata = {
            'title': title,
            'description': description,
            'created': ui.project.get_current_date(),
            'template': template['name']
        }

        if ui.project.create_page(path, template['name'], metadata):
            ui.status_bar.update(f"Page created successfully at {path}", 2)
        else:
            ui.status_bar.update("Failed to create page", 2, error=True)
    except ValueError:
        ui.status_bar.update("Invalid input", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error creating page: {str(e)}", 2, error=True)
