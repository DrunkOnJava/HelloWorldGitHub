"""Main menu implementation."""

from ..models.menu_item import MenuItem
from .development_menu import show_development_menu
from .testing_menu import show_testing_menu
from .github_menu import show_github_menu
from .deployment_menu import show_deployment_menu
from .mcp_menu import show_mcp_menu
from .project_menu import show_project_menu
from .performance_menu import PerformanceMenu
from .security_menu import SecurityMenu
from .database_menu import DatabaseMenu
from .asset_menu import AssetMenu
from .config_menu import ConfigMenu
from .logging_menu import LoggingMenu
from .analytics_menu import AnalyticsMenu

def show_analytics_menu(ui, project_manager) -> None:
    """Show analytics menu."""
    menu = AnalyticsMenu(project_manager.project_root)
    while True:
        ui.print_header(
            "Analytics Integration",
            "Track usage, performance, and generate reports"
        )
        menu_items = menu.get_menu_items()
        menu_items.append(
            MenuItem(
                key="back",
                label="Back",
                description="Return to main menu",
                callback=lambda: True
            )
        )

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == "back" or choice():
            break

def show_logging_menu(ui, project_manager) -> None:
    """Show logging and monitoring menu."""
    menu = LoggingMenu(ui, project_manager.logging_manager)
    while True:
        ui.print_header(
            "Logging and Monitoring",
            "Manage logs, configure levels, and analyze trends"
        )
        menu_items = menu.get_menu_items()
        menu_items.append(
            MenuItem(
                key="back",
                label="Back",
                description="Return to main menu",
                callback=lambda: True
            )
        )

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == "back" or choice():
            break

def show_config_menu(ui, project_manager) -> None:
    """Show configuration management menu."""
    menu = ConfigMenu(ui, project_manager.config_manager)
    while True:
        ui.print_header(
            "Configuration Management",
            "Manage environments, builds, and secrets"
        )
        menu_items = menu.get_menu_items()
        menu_items.append(
            MenuItem(
                key="back",
                label="Back",
                description="Return to main menu",
                callback=lambda: True
            )
        )

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == "back" or choice():
            break

def show_asset_menu(ui, project_manager) -> None:
    """Show asset management menu."""
    menu = AssetMenu(ui, project_manager)
    while True:
        ui.print_header(
            "Asset Management",
            "Manage project assets including images and fonts"
        )
        menu_items = menu.get_menu_items()
        menu_items.append(
            MenuItem(
                key="back",
                label="Back",
                description="Return to main menu",
                callback=lambda: True
            )
        )

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == "back" or choice():
            break

def show_database_menu(ui, project_manager) -> None:
    """Show database tools menu."""
    menu = DatabaseMenu(ui, project_manager)
    while True:
        ui.print_header(
            "Database Tools",
            "Manage databases and data"
        )
        menu_items = menu.get_menu_items()
        menu_items.append(
            MenuItem(
                key="back",
                label="Back",
                description="Return to main menu",
                callback=lambda: True
            )
        )

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == "back" or choice():
            break

def show_security_menu(ui, project_manager) -> None:
    """Show security tools menu."""
    menu = SecurityMenu(ui, project_manager)
    while True:
        ui.print_header(
            "Security Tools",
            "Manage security features and configurations"
        )
        menu_items = menu.get_menu_items()
        menu_items.append(
            MenuItem(
                key="back",
                label="Back",
                description="Return to main menu",
                callback=lambda: True
            )
        )

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == "back" or choice():
            break

def show_performance_menu(ui, project_manager) -> None:
    """Show performance tools menu."""
    menu = PerformanceMenu(ui, project_manager)
    while True:
        ui.print_header(
            "Performance Tools",
            "Monitor and optimize performance"
        )
        menu_items = menu.get_menu_items()
        menu_items.append(
            MenuItem(
                key="back",
                label="Back",
                description="Return to main menu",
                callback=lambda: True
            )
        )

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == "back" or choice():
            break

def main_menu(ui, project_manager) -> None:
    """Main menu implementation."""
    while True:
        ui.print_header(
            "HelloWorldGitHub CLI",
            "Project Management Interface"
        )

        menu_items = [
            MenuItem(
                key='development',
                label='Development',
                description='Run development server, build, and preview',
                icon='🚀',
                shortcut='d'
            ),
            MenuItem(
                key='testing',
                label='Testing',
                description='Run tests and view coverage',
                icon='🧪',
                shortcut='t'
            ),
            MenuItem(
                key='github',
                label='GitHub',
                description='Manage GitHub repository and features',
                icon='🌐',
                shortcut='g'
            ),
            MenuItem(
                key='deployment',
                label='Deployment',
                description='Manage environments, releases, and deployments',
                icon='🚀',
                shortcut='y'
            ),
            MenuItem(
                key='mcp',
                label='MCP Tools',
                description='Access MCP tools and utilities',
                icon='🛠️',
                shortcut='m'
            ),
            MenuItem(
                key='project',
                label='Project Tools',
                description='Project-specific utilities and generators',
                icon='📁',
                shortcut='p'
            ),
            MenuItem(
                key='performance',
                label='Performance Tools',
                description='Monitor and optimize performance',
                icon='📊',
                shortcut='r'
            ),
            MenuItem(
                key='security',
                label='Security Tools',
                description='Manage security features and configurations',
                icon='🔒',
                shortcut='s'
            ),
            MenuItem(
                key="database",
                label="Database Tools",
                description="Manage databases and data",
                icon="🗄️",
                shortcut="b"
            ),
            MenuItem(
                key="assets",
                label="Asset Management",
                description="Manage project assets including images and fonts",
                icon="🖼️",
                shortcut="a"
            ),
            MenuItem(
                key="config",
                label="Configuration",
                description="Manage environments, builds, and secrets",
                icon="⚙️",
                shortcut="c"
            ),
            MenuItem(
                key="logging",
                label="Logging",
                description="Manage logs, configure levels, and analyze trends",
                icon="📝",
                shortcut="l"
            ),
            MenuItem(
                key="analytics",
                label="Analytics",
                description="Track usage, performance, and generate reports",
                icon="📊",
                shortcut="n"
            ),
            MenuItem(
                key="help",
                label="Help",
                description="Show help information",
                icon="❓",
                shortcut="h"
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'development':
            show_development_menu(ui, project_manager)
        elif choice == 'testing':
            show_testing_menu(ui, project_manager)
        elif choice == 'github':
            show_github_menu(ui, project_manager)
        elif choice == 'deployment':
            show_deployment_menu(ui, project_manager)
        elif choice == 'mcp':
            show_mcp_menu(ui, project_manager)
        elif choice == 'project':
            show_project_menu(ui, project_manager)
        elif choice == 'performance':
            show_performance_menu(ui, project_manager)
        elif choice == 'security':
            show_security_menu(ui, project_manager)
        elif choice == "database":
            show_database_menu(ui, project_manager)
        elif choice == "assets":
            show_asset_menu(ui, project_manager)
        elif choice == "config":
            show_config_menu(ui, project_manager)
        elif choice == "logging":
            show_logging_menu(ui, project_manager)
        elif choice == "analytics":
            show_analytics_menu(ui, project_manager)
        elif choice == "help":
            ui.show_help()
