"""Optimization tools submenu implementation."""

from ...models.menu_item import MenuItem
from ...project.project_manager import get_project_root

def show_optimization_submenu(ui) -> None:
    """Optimization tools submenu."""
    while True:
        ui.print_header(
            "Optimization Tools",
            "Performance Optimization"
        )

        menu_items = [
            MenuItem(
                key='pages',
                label='Pages Optimizer',
                description='Optimize GitHub Pages',
                icon='🌐',
                shortcut='p'
            ),
            MenuItem(
                key='assets',
                label='Asset Optimization',
                description='Optimize images and assets',
                icon='🖼️',
                shortcut='a'
            ),
            MenuItem(
                key='performance',
                label='Performance Analysis',
                description='Analyze site performance',
                icon='⚡',
                shortcut='f'
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
        elif choice == 'pages':
            ui.status_bar.update("Optimizing GitHub Pages...", 1)
            try:
                project_root = get_project_root()

                # First analyze the site
                analysis = ui.use_mcp_tool(
                    'github-pages-optimizer',
                    'analyze_site',
                    {
                        'projectPath': project_root,
                        'baseUrl': '/HelloWorldGitHub/'
                    }
                )

                if analysis.get('suggestions', []):
                    ui.print_info("Optimization Suggestions:")
                    for suggestion in analysis['suggestions']:
                        ui.print_info(f"- {suggestion}")

                    apply = ui.get_input("Would you like to apply optimizations? (y/n)", [
                        MenuItem(key='y', label='Yes', shortcut='y'),
                        MenuItem(key='n', label='No', shortcut='n')
                    ])

                    if apply == 'y':
                        result = ui.use_mcp_tool(
                            'github-pages-optimizer',
                            'apply_optimizations',
                            {
                                'projectPath': project_root,
                                'optimizations': analysis['optimizations']
                            }
                        )
                        if result.get('applied', 0) > 0:
                            ui.print_success(f"Applied {result['applied']} optimizations!")
                            for change in result.get('changes', []):
                                ui.print_info(f"- {change}")
                        else:
                            ui.print_info("No optimizations were applied")
                else:
                    ui.print_success("No optimization suggestions found!")
            except Exception as e:
                ui.print_error(f"Error optimizing GitHub Pages: {str(e)}")
            ui.status_bar.update("Pages optimization complete", 2)
        elif choice == 'assets':
            ui.status_bar.update("Optimizing assets...", 1)
            try:
                project_root = get_project_root()

                # Use icon-generator for SVG optimization
                icon_result = ui.use_mcp_tool(
                    'icon-generator',
                    'generate_icons',
                    {
                        'svgPath': f"{project_root}/src/assets/icon.svg",
                        'outputDir': f"{project_root}/public/icons"
                    }
                )

                if icon_result.get('generated', 0) > 0:
                    ui.print_success(f"Optimized {icon_result['generated']} icons!")
                else:
                    ui.print_info("No icons needed optimization")

                # Use github-pages-optimizer for other assets
                asset_result = ui.use_mcp_tool(
                    'github-pages-optimizer',
                    'analyze_site',
                    {
                        'projectPath': project_root,
                        'baseUrl': '/HelloWorldGitHub/'
                    }
                )

                if asset_result.get('assetSuggestions', []):
                    ui.print_info("\nAsset Optimization Suggestions:")
                    for suggestion in asset_result['assetSuggestions']:
                        ui.print_info(f"- {suggestion}")
                else:
                    ui.print_success("No asset optimizations needed!")
            except Exception as e:
                ui.print_error(f"Error optimizing assets: {str(e)}")
            ui.status_bar.update("Asset optimization complete", 2)
        elif choice == 'performance':
            ui.status_bar.update("Analyzing performance...", 1)
            try:
                project_root = get_project_root()

                # Use github-pages-optimizer for performance analysis
                result = ui.use_mcp_tool(
                    'github-pages-optimizer',
                    'analyze_site',
                    {
                        'projectPath': project_root,
                        'baseUrl': '/HelloWorldGitHub/'
                    }
                )

                if result:
                    ui.print_info("Performance Analysis:")
                    if 'performance' in result:
                        ui.print_info(f"\nPerformance Score: {result['performance']}")
                    if 'metrics' in result:
                        ui.print_info("\nKey Metrics:")
                        for metric, value in result['metrics'].items():
                            ui.print_info(f"- {metric}: {value}")
                    if 'suggestions' in result:
                        ui.print_info("\nPerformance Suggestions:")
                        for suggestion in result['suggestions']:
                            ui.print_info(f"- {suggestion}")
                else:
                    ui.print_warning("No performance data available")
            except Exception as e:
                ui.print_error(f"Error analyzing performance: {str(e)}")
            ui.status_bar.update("Performance analysis complete", 2)
