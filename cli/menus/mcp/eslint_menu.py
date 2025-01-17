"""ESLint tools submenu implementation."""

from ...models.menu_item import MenuItem
from ...project.project_manager import get_project_root

def show_eslint_submenu(ui) -> None:
    """ESLint tools submenu."""
    while True:
        ui.print_header(
            "ESLint Tools",
            "ESLint Configuration and Fixes"
        )

        menu_items = [
            MenuItem(
                key='check',
                label='Check Issues',
                description='Check for ESLint errors',
                icon='🔍',
                shortcut='c'
            ),
            MenuItem(
                key='fix',
                label='Fix Issues',
                description='Automatically fix ESLint errors',
                icon='🔧',
                shortcut='f'
            ),
            MenuItem(
                key='rules',
                label='Rule Management',
                description='Configure ESLint rules',
                icon='📋',
                shortcut='r'
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
            ui.status_bar.update("Checking ESLint issues...", 1)
            try:
                project_root = get_project_root()

                # Use MCP eslint-fixer tool to check for errors
                result = ui.use_mcp_tool(
                    'eslint-fixer',
                    'check_lint_errors',
                    {'path': project_root}
                )

                if result.get('errors', []):
                    ui.print_warning(f"Found {len(result['errors'])} ESLint issues:")
                    for error in result['errors']:
                        ui.print_error(f"{error['file']}:{error['line']} - {error['message']}")
                else:
                    ui.print_success("No ESLint issues found!")
            except Exception as e:
                ui.print_error(f"Error checking ESLint issues: {str(e)}")
            ui.status_bar.update("ESLint check complete", 2)
        elif choice == 'fix':
            ui.status_bar.update("Fixing ESLint issues...", 1)
            try:
                project_root = get_project_root()

                # Use MCP eslint-fixer tool to fix errors
                result = ui.use_mcp_tool(
                    'eslint-fixer',
                    'fix_lint_errors',
                    {'path': project_root}
                )

                if result.get('fixed', 0) > 0:
                    ui.print_success(f"Fixed {result['fixed']} ESLint issues!")
                else:
                    ui.print_info("No issues needed fixing")
            except Exception as e:
                ui.print_error(f"Error fixing ESLint issues: {str(e)}")
            ui.status_bar.update("ESLint fix complete", 2)
        elif choice == 'rules':
            ui.status_bar.update("Managing ESLint rules...", 1)
            try:
                project_root = get_project_root()

                # Use MCP eslint-fixer tool to analyze rules
                result = ui.use_mcp_tool(
                    'eslint-fixer',
                    'analyze_errors',
                    {'path': project_root}
                )

                if result.get('rules', {}):
                    ui.print_info("Current ESLint rule violations:")
                    for rule, count in result['rules'].items():
                        ui.print_info(f"{rule}: {count} violations")

                        # Get detailed rule explanation
                        explanation = ui.use_mcp_tool(
                            'eslint-fixer',
                            'explain_rule',
                            {'rule': rule}
                        )
                        if explanation.get('description'):
                            ui.print_info(f"Description: {explanation['description']}")
                else:
                    ui.print_success("No rule violations found!")
            except Exception as e:
                ui.print_error(f"Error analyzing ESLint rules: {str(e)}")
            ui.status_bar.update("Rule analysis complete", 2)
