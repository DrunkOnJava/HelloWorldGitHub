"""Project tools submenu implementation."""

from ...models.menu_item import MenuItem
from ...project.project_manager import get_project_root

def show_project_tools_submenu(ui) -> None:
    """Project tools submenu."""
    while True:
        ui.print_header(
            "Project Tools",
            "Project Management Utilities"
        )

        menu_items = [
            MenuItem(
                key='links',
                label='Link Handler',
                description='Validate and fix links',
                icon='🔗',
                shortcut='l'
            ),
            MenuItem(
                key='icons',
                label='Icon Generator',
                description='Generate optimized icons',
                icon='🎨',
                shortcut='i'
            ),
            MenuItem(
                key='index',
                label='Index Generator',
                description='Generate index files',
                icon='📑',
                shortcut='g'
            ),
            MenuItem(
                key='back',
                label='Back to MCP Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'links':
            ui.status_bar.update("Managing links...", 1)
            try:
                project_root = get_project_root()

                # First validate links
                validate_result = ui.use_mcp_tool(
                    'link-handler',
                    'validate_links',
                    {'directory': project_root}
                )

                if validate_result.get('broken', []):
                    ui.print_warning(f"Found {len(validate_result['broken'])} broken links")
                    fix = ui.get_input("Would you like to fix broken links? (y/n)", [
                        MenuItem(key='y', label='Yes', shortcut='y'),
                        MenuItem(key='n', label='No', shortcut='n')
                    ])

                    if fix == 'y':
                        fix_result = ui.use_mcp_tool(
                            'link-handler',
                            'fix_links',
                            {'directory': project_root}
                        )
                        if fix_result.get('fixed', 0) > 0:
                            ui.print_success(f"Fixed {fix_result['fixed']} links!")
                        else:
                            ui.print_info("No links could be automatically fixed")
                else:
                    ui.print_success("No broken links found!")

                # Get page relationships
                relationships = ui.use_mcp_tool(
                    'link-handler',
                    'get_page_relationships',
                    {'directory': project_root}
                )

                if relationships.get('connections', []):
                    ui.print_info("\nPage Relationships:")
                    for connection in relationships['connections']:
                        ui.print_info(f"- {connection['from']} -> {connection['to']}")
                else:
                    ui.print_info("No page relationships found")

            except Exception as e:
                ui.print_error(f"Error managing links: {str(e)}")
            ui.status_bar.update("Link management complete", 2)
        elif choice == 'icons':
            ui.status_bar.update("Generating icons...", 1)
            try:
                project_root = get_project_root()

                # Use MCP icon-generator tool
                result = ui.use_mcp_tool(
                    'icon-generator',
                    'generate_icons',
                    {
                        'svgPath': f"{project_root}/src/assets/icon.svg",
                        'outputDir': f"{project_root}/public/icons"
                    }
                )

                if result.get('generated', 0) > 0:
                    ui.print_success(f"Generated {result['generated']} icons!")
                    for size, path in result.get('files', {}).items():
                        ui.print_info(f"- {size}: {path}")
                else:
                    ui.print_warning("No icons were generated. Make sure source SVG exists.")
            except Exception as e:
                ui.print_error(f"Error generating icons: {str(e)}")
            ui.status_bar.update("Icon generation complete", 2)
        elif choice == 'index':
            ui.status_bar.update("Generating index files...", 1)
            try:
                project_root = get_project_root()

                # Use MCP index-generator tool
                result = ui.use_mcp_tool(
                    'index-generator',
                    'generate_index_files',
                    {
                        'projectPath': project_root,
                        'excludeDirs': ['node_modules', '.git', 'dist', 'build']
                    }
                )

                if result.get('generated', 0) > 0:
                    ui.print_success(f"Generated {result['generated']} index files!")
                    for dir_path in result.get('directories', []):
                        ui.print_info(f"- Created index.html in {dir_path}")
                else:
                    ui.print_info("No index files needed to be generated")
            except Exception as e:
                ui.print_error(f"Error generating index files: {str(e)}")
            ui.status_bar.update("Index generation complete", 2)
