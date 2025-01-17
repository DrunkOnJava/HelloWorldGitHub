"""Bundle menu implementation."""

from ...models.menu_item import MenuItem

def show_bundle_submenu(ui) -> None:
    """Bundle analysis submenu."""
    while True:
        ui.print_header(
            "Bundle Analysis",
            "Analyze and Optimize Bundles"
        )

        menu_items = [
            MenuItem(
                key='analyze',
                label='Analyze Bundle',
                description='Analyze bundle size and composition',
                icon='📊',
                shortcut='a'
            ),
            MenuItem(
                key='deps',
                label='Dependencies',
                description='Analyze dependencies',
                icon='🔗',
                shortcut='d'
            ),
            MenuItem(
                key='unused',
                label='Unused Code',
                description='Find unused code and imports',
                icon='🗑️',
                shortcut='u'
            ),
            MenuItem(
                key='optimize',
                label='Optimize',
                description='Optimize bundle size',
                icon='✨',
                shortcut='o'
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
        elif choice == 'analyze':
            analyze_bundle_size(ui)
        elif choice == 'deps':
            analyze_dependencies(ui)
        elif choice == 'unused':
            find_unused_code(ui)
        elif choice == 'optimize':
            optimize_bundle(ui)

def analyze_bundle_size(ui) -> None:
    """Analyze bundle size and composition."""
    if ui.project.analyze_bundle_size():
        ui.status_bar.update("Bundle analysis completed successfully", 3)
    else:
        ui.status_bar.update("Bundle analysis failed", 3)

def analyze_dependencies(ui) -> None:
    """Analyze project dependencies."""
    if ui.project.analyze_dependencies():
        ui.status_bar.update("Dependency analysis completed successfully", 3)
    else:
        ui.status_bar.update("Dependency analysis failed", 3)

def find_unused_code(ui) -> None:
    """Find unused code and imports."""
    if ui.project.find_unused_code():
        ui.status_bar.update("Unused code analysis completed successfully", 3)
    else:
        ui.status_bar.update("Unused code analysis failed", 3)

def optimize_bundle(ui) -> None:
    """Optimize bundle size."""
    if ui.project.optimize_bundle():
        ui.status_bar.update("Bundle optimization completed successfully", 3)
    else:
        ui.status_bar.update("Bundle optimization failed", 3)
