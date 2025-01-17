"""TypeScript tools submenu implementation."""

from ...models.menu_item import MenuItem
from ...project.project_manager import get_project_root

def show_typescript_submenu(ui) -> None:
    """TypeScript tools submenu."""
    while True:
        ui.print_header(
            "TypeScript Tools",
            "TypeScript Validation and Fixes"
        )

        menu_items = [
            MenuItem(
                key='check',
                label='Check Types',
                description='Check TypeScript types',
                icon='🔍',
                shortcut='c'
            ),
            MenuItem(
                key='fix',
                label='Fix Issues',
                description='Fix TypeScript errors',
                icon='🔧',
                shortcut='f'
            ),
            MenuItem(
                key='organize',
                label='Organize Imports',
                description='Clean up imports',
                icon='📋',
                shortcut='o'
            ),
            MenuItem(
                key='back',
                label='Back to Code Quality Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'check':
            ui.status_bar.update("Checking TypeScript types...", 1)
            try:
                project_root = get_project_root()

                # Use MCP typescript-fixer tool to check types
                result = ui.use_mcp_tool(
                    'typescript-fixer',
                    'check_typescript_errors',
                    {'projectPath': project_root}
                )

                if result.get('errors', []):
                    ui.print_warning(f"Found {len(result['errors'])} type errors:")
                    for error in result['errors']:
                        ui.print_error(f"{error['file']}:{error['line']} - {error['message']}")
                else:
                    ui.print_success("No type errors found!")
            except Exception as e:
                ui.print_error(f"Error checking types: {str(e)}")
            ui.status_bar.update("Type check complete", 2)
        elif choice == 'fix':
            ui.status_bar.update("Fixing TypeScript errors...", 1)
            try:
                project_root = get_project_root()

                # Use MCP typescript-fixer tool to fix errors
                result = ui.use_mcp_tool(
                    'typescript-fixer',
                    'fix_typescript_errors',
                    {'projectPath': project_root}
                )

                if result.get('fixed', 0) > 0:
                    ui.print_success(f"Fixed {result['fixed']} type errors!")
                else:
                    ui.print_info("No errors needed fixing")
            except Exception as e:
                ui.print_error(f"Error fixing types: {str(e)}")
            ui.status_bar.update("Type fixes complete", 2)
        elif choice == 'organize':
            ui.status_bar.update("Organizing imports...", 1)
            try:
                project_root = get_project_root()

                # Use MCP typescript-fixer tool to organize imports
                result = ui.use_mcp_tool(
                    'typescript-fixer',
                    'organize_imports',
                    {'projectPath': project_root}
                )

                if result.get('organized', 0) > 0:
                    ui.print_success(f"Organized imports in {result['organized']} files!")
                else:
                    ui.print_info("No imports needed organizing")
            except Exception as e:
                ui.print_error(f"Error organizing imports: {str(e)}")
            ui.status_bar.update("Import organization complete", 2)
