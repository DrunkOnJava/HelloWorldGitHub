"""
Enhanced Terminal UI for HelloWorldGitHub Project
A sophisticated CLI tool for managing the Astro.js project with integrated MCP tools.
"""

import os
from .ui.terminal import TerminalUI
from .menus.main_menu import main_menu
from .project.project_manager import ProjectManager

def main():
    """Main entry point."""
    ui = TerminalUI()
    project_manager = ProjectManager(os.getcwd())
    try:
        main_menu(ui, project_manager)
    except Exception as e:
        ui.print_output(f"\n{ui.theme.COLORS['ERROR']}Error: {str(e)}{ui.theme.COLORS['ENDC']}")
    finally:
        ui.cleanup()

if __name__ == "__main__":
    main()
