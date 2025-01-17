"""Page metadata management menu implementation."""

from ....models.menu_item import MenuItem

def show_metadata_menu(ui) -> None:
    """Page metadata management submenu."""
    while True:
        ui.print_header(
            "Metadata Management",
            "Manage Page Metadata"
        )

        menu_items = [
            MenuItem(
                key='view',
                label='View Metadata',
                description='View page metadata',
                icon='👁️',
                shortcut='v'
            ),
            MenuItem(
                key='edit',
                label='Edit Metadata',
                description='Edit page metadata',
                icon='✏️',
                shortcut='e'
            ),
            MenuItem(
                key='validate',
                label='Validate Metadata',
                description='Check metadata consistency',
                icon='✓',
                shortcut='c'
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
            view_metadata(ui)
        elif choice == 'edit':
            edit_metadata(ui)
        elif choice == 'validate':
            validate_metadata(ui)

def view_metadata(ui) -> None:
    """View page metadata."""
    pages = ui.project.get_pages()
    if not pages:
        ui.status_bar.update("No pages found", 2)
        return

    print("\nSelect page:")
    for i, page in enumerate(pages, 1):
        print(f"{i}. {page['path']}")

    try:
        selection = int(ui.get_input("\nPage number", required=True)) - 1
        if selection < 0 or selection >= len(pages):
            ui.status_bar.update("Invalid selection", 2, error=True)
            return

        page = pages[selection]
        print(f"\n{ui.theme.COLORS['HEADER']}Metadata for {page['path']}{ui.theme.COLORS['ENDC']}")
        for key, value in page['metadata'].items():
            print(f"{key}: {value}")

        print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
        input()
    except ValueError:
        ui.status_bar.update("Invalid input", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error viewing metadata: {str(e)}", 2, error=True)

def edit_metadata(ui) -> None:
    """Edit page metadata."""
    pages = ui.project.get_pages()
    if not pages:
        ui.status_bar.update("No pages found", 2)
        return

    print("\nSelect page:")
    for i, page in enumerate(pages, 1):
        print(f"{i}. {page['path']}")

    try:
        selection = int(ui.get_input("\nPage number", required=True)) - 1
        if selection < 0 or selection >= len(pages):
            ui.status_bar.update("Invalid selection", 2, error=True)
            return

        page = pages[selection]
        print(f"\nEditing metadata for {page['path']}")
        print("Press Enter to keep current values")

        metadata = {}
        for key, value in page['metadata'].items():
            new_value = ui.get_input(f"{key} [{value}]") or value
            metadata[key] = new_value

        if ui.project.update_page_metadata(page['path'], metadata):
            ui.status_bar.update("Metadata updated successfully", 2)
        else:
            ui.status_bar.update("Failed to update metadata", 2, error=True)
    except ValueError:
        ui.status_bar.update("Invalid input", 2, error=True)
    except Exception as e:
        ui.status_bar.update(f"Error editing metadata: {str(e)}", 2, error=True)

def validate_metadata(ui) -> None:
    """Validate page metadata."""
    pages = ui.project.get_pages()
    if not pages:
        ui.status_bar.update("No pages found", 2)
        return

    print("\nValidating page metadata...")
    has_errors = False

    for page in pages:
        errors = ui.project.validate_page_metadata(page['path'])
        if errors:
            has_errors = True
            print(f"\n{ui.theme.COLORS['ERROR']}Errors in {page['path']}:{ui.theme.COLORS['ENDC']}")
            for error in errors:
                print(f"  - {error}")

    if not has_errors:
        print(f"\n{ui.theme.COLORS['SUCCESS']}All metadata is valid!{ui.theme.COLORS['ENDC']}")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()
