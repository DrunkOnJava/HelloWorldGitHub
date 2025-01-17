"""Page structure management menu implementation."""

from ....models.menu_item import MenuItem

def show_structure_menu(ui) -> None:
    """Page structure management submenu."""
    while True:
        ui.print_header(
            "Page Structure",
            "Manage Page Hierarchy"
        )

        menu_items = [
            MenuItem(
                key='view',
                label='View Structure',
                description='Display page hierarchy',
                icon='🌳',
                shortcut='v'
            ),
            MenuItem(
                key='move',
                label='Move Page',
                description='Move page to new location',
                icon='📦',
                shortcut='m'
            ),
            MenuItem(
                key='rename',
                label='Rename Page',
                description='Rename page and update links',
                icon='✏️',
                shortcut='r'
            ),
            MenuItem(
                key='delete',
                label='Delete Page',
                description='Remove page and clean up',
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
        elif choice == 'view':
            view_structure(ui)
        elif choice == 'move':
            move_page(ui)
        elif choice == 'rename':
            rename_page(ui)
        elif choice == 'delete':
            delete_page(ui)

def view_structure(ui) -> None:
    """Display page hierarchy."""
    pages = ui.project.get_pages()
    if not pages:
        ui.status_bar.update("No pages found", 2)
        return

    print("\nPage Structure:")
    for page in pages:
        print(f"\n{ui.theme.COLORS['HEADER']}{page['path']}{ui.theme.COLORS['ENDC']}")
        print(f"Title: {page['metadata']['title']}")
        print(f"Template: {page['metadata']['template']}")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()

def move_page(ui) -> None:
    """Move page to new location."""
    pages = ui.project.get_pages()
    if not pages:
        ui.status_bar.update("No pages found", 2)
        return

    print("\nSelect page to move:")
    for i, page in enumerate(pages, 1):
        print(f"{i}. {page['path']}")

    try:
        selection = int(ui.get_input("\nPage number", required=True)) - 1
        if selection < 0 or selection >= len(pages):
            ui.status_bar.update("Invalid selection", 2, error=True)
            return

        page = pages[selection]
        new_path = ui.get_input("New path", required=True)

        if ui.project.move_page(page['path'], new_path):
            ui.status_bar.update(f"Page moved to {new_path}", 2)
        else:
            ui.status_bar.update("Failed to move page", 2, error=True)
    except ValueError:
        ui.status_bar.update("Invalid input", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error moving page: {str(e)}", 2, error=True)

def rename_page(ui) -> None:
    """Rename page and update links."""
    pages = ui.project.get_pages()
    if not pages:
        ui.status_bar.update("No pages found", 2)
        return

    print("\nSelect page to rename:")
    for i, page in enumerate(pages, 1):
        print(f"{i}. {page['path']}")

    try:
        selection = int(ui.get_input("\nPage number", required=True)) - 1
        if selection < 0 or selection >= len(pages):
            ui.status_bar.update("Invalid selection", 2, error=True)
            return

        page = pages[selection]
        new_name = ui.get_input("New name", required=True)

        if ui.project.rename_page(page['path'], new_name):
            ui.status_bar.update(f"Page renamed to {new_name}", 2)
        else:
            ui.status_bar.update("Failed to rename page", 2, error=True)
    except ValueError:
        ui.status_bar.update("Invalid input", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error renaming page: {str(e)}", 2, error=True)

def delete_page(ui) -> None:
    """Delete page and clean up."""
    pages = ui.project.get_pages()
    if not pages:
        ui.status_bar.update("No pages found", 2)
        return

    print("\nSelect page to delete:")
    for i, page in enumerate(pages, 1):
        print(f"{i}. {page['path']}")

    try:
        selection = int(ui.get_input("\nPage number", required=True)) - 1
        if selection < 0 or selection >= len(pages):
            ui.status_bar.update("Invalid selection", 2, error=True)
            return

        page = pages[selection]
        confirm = ui.get_input(f"Are you sure you want to delete '{page['path']}'? (y/n)").lower()
        if confirm == 'y':
            if ui.project.delete_page(page['path']):
                ui.status_bar.update(f"Page deleted successfully", 2)
            else:
                ui.status_bar.update("Failed to delete page", 2, error=True)
    except ValueError:
        ui.status_bar.update("Invalid input", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error deleting page: {str(e)}", 2, error=True)
