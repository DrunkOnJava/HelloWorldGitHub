"""Enhanced Terminal UI implementation."""

import os
import sys
import shutil
import signal
from typing import List, Any

from cli.logger import log_input, log_output
from ..models.menu_item import MenuItem
from ..theme.theme import Theme
from ..project.project_manager import ProjectManager
from .status_bar import StatusBar

class TerminalUI:
    """Enhanced Terminal UI with project-specific features."""
    def __init__(self):
        self.theme = Theme()
        self.terminal_width = shutil.get_terminal_size().columns
        self.terminal_height = shutil.get_terminal_size().lines
        self.status_bar = StatusBar(self)
        self.project = ProjectManager(self)

        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)

    def _handle_interrupt(self, signum: int, frame: Any) -> None:
        """Handle interrupt signals gracefully."""
        self.status_bar.update("Caught interrupt signal, press again to exit")
        signal.signal(signum, signal.default_int_handler)

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_header(self, title: str, subtitle: str = "") -> None:
        """Print a beautifully styled header with optional subtitle."""
        self.clear_screen()
        width = self.terminal_width

        header = f"{self.theme.COLORS['HEADER']}{self.theme.COLORS['BOLD']}{title}{self.theme.COLORS['ENDC']}"
        if subtitle:
            header += f"\n{self.theme.COLORS['SECONDARY']}{subtitle}{self.theme.COLORS['ENDC']}"

        print("\n" + "═" * width)
        print(header.center(width))
        print("═" * width + "\n")

    def print_menu(self, items: List[MenuItem]) -> None:
        """Display a beautifully formatted menu with icons and descriptions."""
        for idx, item in enumerate(items, 1):
            if item.key in ['help', 'back', 'exit']:
                continue

            number = f"{self.theme.COLORS['SECONDARY']}[{idx}]{self.theme.COLORS['ENDC']}"
            icon = f"{self.theme.COLORS['PRIMARY']}{item.icon}{self.theme.COLORS['ENDC']}"
            label = item.label

            if item.disabled:
                label = f"{self.theme.COLORS['SECONDARY']}{label} (Disabled){self.theme.COLORS['ENDC']}"

            shortcut = f" {self.theme.COLORS['SECONDARY']}({item.shortcut}){self.theme.COLORS['ENDC']}" if item.shortcut else ""

            print(f" {number} {icon} {label}{shortcut}")

            if item.description:
                desc = f"{self.theme.COLORS['SECONDARY']}{item.description}{self.theme.COLORS['ENDC']}"
                print(f"    {self.theme.SYMBOLS['arrow']} {desc}")

        print("\n" + self.theme.COLORS['SECONDARY'] + "─" * self.terminal_width + self.theme.COLORS['ENDC'])
        print(f" {self.theme.COLORS['INFO']}[h] Help{self.theme.COLORS['ENDC']}  {self.theme.COLORS['WARNING']}[b] Back{self.theme.COLORS['ENDC']}  {self.theme.COLORS['ERROR']}[x] Exit{self.theme.COLORS['ENDC']}")

    def get_input(self, prompt: str = "Enter your choice", items: List[MenuItem] = None, required: bool = False) -> str:
        """Get user input with validation."""
        while True:
            try:
                user_input = input(f"\n{self.theme.COLORS['BOLD']}{prompt}: {self.theme.COLORS['ENDC']}")
                log_input(user_input)

                # For menu selection
                if items is not None:
                    choice = user_input.lower()
                    if not choice:
                        self.status_bar.update("Please enter a valid choice", 2)
                        continue

                    if choice in ['x', 'q']:
                        if self._confirm_action("Are you sure you want to exit?"):
                            self.cleanup()
                            sys.exit(0)
                    elif choice == 'h':
                        self.show_help()
                        return 'help'
                    elif choice == 'b':
                        return 'back'

                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(items):
                            item = items[idx]
                            if item.disabled:
                                self.status_bar.update("This option is currently disabled", 2)
                                continue
                            if item.requires_confirmation:
                                if not self._confirm_action(f"Are you sure you want to {item.label.lower()}?"):
                                    continue
                            return item.key

                    for item in items:
                        if item.shortcut and choice == item.shortcut.lower():
                            return item.key

                    self.status_bar.update("Invalid choice, please try again", 2)
                    continue

                # For general input
                if required and not choice.strip():
                    self.status_bar.update("This field is required", 2)
                    continue

                return choice.strip()

            except EOFError:
                self._handle_interrupt(None, None)
            except KeyboardInterrupt:
                print("\n")
                self.status_bar.update("Use 'x' to exit", 2)

    def print_output(self, output: str) -> None:
        """Print output to the terminal and log it."""
        print(output)
        log_output(output)

    def _confirm_action(self, prompt: str) -> bool:
        """Ask for user confirmation."""
        response = input(f"\n{self.theme.COLORS['WARNING']}{prompt} (y/N): {self.theme.COLORS['ENDC']}")
        return response.lower() == 'y'

    def cleanup(self) -> None:
        """Clean up resources before exit."""
        self.status_bar.stop()
        self.clear_screen()
        print(f"\n{self.theme.COLORS['SUCCESS']}Thanks for using HelloWorldGitHub CLI!{self.theme.COLORS['ENDC']}\n")

    def show_help(self) -> None:
        """Show help information."""
        self.print_header(
            "Help & Information",
            "Command Reference and Tips"
        )

        sections = [
            ("Navigation", [
                ("Number Keys (1-9)", "Select menu items directly"),
                ("Shortcuts", "Quick access to menu items (shown in parentheses)"),
                ("b or Back", "Return to previous menu"),
                ("h or Help", "Show this help screen"),
                ("x or Exit", "Exit the program"),
            ]),
            ("Development", [
                ("Development Server", "Run 'npm run dev' for local development"),
                ("Build", "Build project for production"),
                ("Preview", "Preview production build locally"),
                ("CSS", "Build or watch Tailwind CSS"),
            ]),
            ("Testing", [
                ("Run Tests", "Execute all tests"),
                ("Watch Mode", "Run tests on file changes"),
                ("Coverage", "Generate test coverage report"),
            ]),
            ("MCP Tools", [
                ("ESLint Fixer", "Automatically fix ESLint issues"),
                ("TypeScript Fixer", "Fix TypeScript errors"),
                ("Code Analyzer", "Analyze code quality"),
                ("Link Handler", "Validate and fix links"),
            ])
        ]

        for section_title, items in sections:
            print(f"\n{self.theme.COLORS['BOLD']}{section_title}:{self.theme.COLORS['ENDC']}")
            for command, desc in items:
                print(f"  {self.theme.COLORS['PRIMARY']}{command}{self.theme.COLORS['ENDC']}")
                print(f"    {self.theme.SYMBOLS['arrow']} {desc}")

        input(f"\n{self.theme.COLORS['SUCCESS']}Press Enter to continue...{self.theme.COLORS['ENDC']}")

    def print_output(self, output: str) -> None:
        """Print output to the terminal and log it."""
        print(output)
        log_output(output)
