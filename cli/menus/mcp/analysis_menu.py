"""Code analysis submenu implementation."""

from ...models.menu_item import MenuItem
from ...project.project_manager import get_project_root

def show_analysis_submenu(ui) -> None:
    """Code analysis submenu."""
    while True:
        ui.print_header(
            "Code Analysis",
            "Code Quality Analysis Tools"
        )

        menu_items = [
            MenuItem(
                key='analyze',
                label='Analyze Code',
                description='Run code analysis',
                icon='🔍',
                shortcut='a'
            ),
            MenuItem(
                key='metrics',
                label='Code Metrics',
                description='View code quality metrics',
                icon='📊',
                shortcut='m'
            ),
            MenuItem(
                key='suggest',
                label='Suggestions',
                description='Get improvement suggestions',
                icon='💡',
                shortcut='s'
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
        elif choice == 'analyze':
            ui.status_bar.update("Analyzing code...", 1)
            try:
                project_root = get_project_root()

                # Use MCP code-analyzer tool to analyze code
                result = ui.use_mcp_tool(
                    'code-analyzer',
                    'analyze_code',
                    {'directory': project_root}
                )

                if result:
                    ui.print_info("Code Analysis Results:")
                    if 'lineCount' in result:
                        ui.print_info(f"Total lines of code: {result['lineCount']}")
                    if 'suggestions' in result:
                        ui.print_info("\nModularization Suggestions:")
                        for suggestion in result['suggestions']:
                            ui.print_info(f"- {suggestion}")
                else:
                    ui.print_warning("No analysis results available")
            except Exception as e:
                ui.print_error(f"Error analyzing code: {str(e)}")
            ui.status_bar.update("Code analysis complete", 2)
        elif choice == 'metrics':
            ui.status_bar.update("Calculating code metrics...", 1)
            try:
                project_root = get_project_root()

                # Use TypeScript analyzer for code quality metrics
                result = ui.use_mcp_tool(
                    'typescript-fixer',
                    'analyze_code_quality',
                    {'projectPath': project_root}
                )

                if result:
                    ui.print_info("Code Quality Metrics:")
                    if 'complexity' in result:
                        ui.print_info(f"Average complexity: {result['complexity']}")
                    if 'maintainability' in result:
                        ui.print_info(f"Maintainability index: {result['maintainability']}")
                    if 'issues' in result:
                        ui.print_info("\nQuality Issues:")
                        for issue in result['issues']:
                            ui.print_warning(f"- {issue}")
                else:
                    ui.print_warning("No metrics available")
            except Exception as e:
                ui.print_error(f"Error calculating metrics: {str(e)}")
            ui.status_bar.update("Metrics calculation complete", 2)
        elif choice == 'suggest':
            ui.status_bar.update("Generating suggestions...", 1)
            try:
                project_root = get_project_root()

                # Use TypeScript analyzer for type suggestions
                type_result = ui.use_mcp_tool(
                    'typescript-fixer',
                    'suggest_types',
                    {'projectPath': project_root}
                )

                ui.print_info("Code Improvement Suggestions:")

                if type_result.get('suggestions', []):
                    ui.print_info("\nType Suggestions:")
                    for suggestion in type_result['suggestions']:
                        ui.print_info(f"- {suggestion}")

                # Use code analyzer for general suggestions
                code_result = ui.use_mcp_tool(
                    'code-analyzer',
                    'analyze_code',
                    {'directory': project_root}
                )

                if code_result.get('suggestions', []):
                    ui.print_info("\nCode Structure Suggestions:")
                    for suggestion in code_result['suggestions']:
                        ui.print_info(f"- {suggestion}")

                if not type_result.get('suggestions') and not code_result.get('suggestions'):
                    ui.print_warning("No suggestions available")
            except Exception as e:
                ui.print_error(f"Error generating suggestions: {str(e)}")
            ui.status_bar.update("Suggestions complete", 2)
