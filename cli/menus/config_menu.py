"""Configuration management menu."""

from typing import List
from ..models.menu_item import MenuItem
from ..project.config_manager import ConfigManager

class ConfigMenu:
    """Handles configuration management menu operations."""

    def __init__(self, ui, config_manager: ConfigManager):
        self.ui = ui
        self.config_manager = config_manager

    def get_menu_items(self) -> List[MenuItem]:
        """Get configuration management menu items."""
        return [
            MenuItem(
                "Environment Management",
                "Manage environment configurations",
                self.environment_management_menu
            ),
            MenuItem(
                "Build Configuration",
                "Manage build settings and modes",
                self.build_configuration_menu
            ),
            MenuItem(
                "Secret Management",
                "Rotate and manage sensitive configuration",
                self.secret_management_menu
            )
        ]

    def environment_management_menu(self):
        """Show environment management submenu."""
        items = [
            MenuItem(
                "List Environments",
                "Show available environment configurations",
                self._list_environments
            ),
            MenuItem(
                "Save Current Environment",
                "Save current environment configuration",
                self._save_environment
            ),
            MenuItem(
                "Load Environment",
                "Load a saved environment configuration",
                self._load_environment
            ),
            MenuItem(
                "Compare Environments",
                "Compare two environment configurations",
                self._compare_environments
            ),
            MenuItem(
                "Show Current Environment",
                "Display current environment variables",
                self._show_current_environment
            )
        ]
        return items

    def build_configuration_menu(self):
        """Show build configuration submenu."""
        items = [
            MenuItem(
                "Show Build Config",
                "Display current build configuration",
                self._show_build_config
            ),
            MenuItem(
                "Set Build Mode",
                "Set build mode (development/production/staging)",
                self._set_build_mode
            ),
            MenuItem(
                "Update Build Settings",
                "Modify build configuration settings",
                self._update_build_settings
            ),
            MenuItem(
                "Configure Host",
                "Set development server host and port",
                self._configure_host
            )
        ]
        return items

    def secret_management_menu(self):
        """Show secret management submenu."""
        items = [
            MenuItem(
                "Rotate Secrets",
                "Rotate sensitive configuration values",
                self._rotate_secrets
            ),
            MenuItem(
                "Show Secret Status",
                "Display information about secret configurations",
                self._show_secret_status
            )
        ]
        return items

    def _list_environments(self):
        """List available environment configurations."""
        envs = self.config_manager.get_environments()
        if envs:
            print("\nAvailable environments:")
            for env in envs:
                print(f"- {env}")
        else:
            print("\nNo saved environments found")

    def _save_environment(self):
        """Save current environment configuration."""
        name = input("\nEnter name for environment configuration: ")
        if name:
            self.config_manager.save_environment(name)
        else:
            print("\nEnvironment name cannot be empty")

    def _load_environment(self):
        """Load a saved environment configuration."""
        envs = self.config_manager.get_environments()
        if not envs:
            print("\nNo saved environments available")
            return

        print("\nAvailable environments:")
        for i, env in enumerate(envs, 1):
            print(f"{i}. {env}")

        try:
            choice = int(input("\nSelect environment to load (number): "))
            if 1 <= choice <= len(envs):
                self.config_manager.load_environment(envs[choice-1])
            else:
                print("\nInvalid selection")
        except ValueError:
            print("\nInvalid input")

    def _compare_environments(self):
        """Compare two environment configurations."""
        envs = self.config_manager.get_environments()
        if len(envs) < 2:
            print("\nNeed at least two environments to compare")
            return

        print("\nAvailable environments:")
        for i, env in enumerate(envs, 1):
            print(f"{i}. {env}")

        try:
            env1_idx = int(input("\nSelect first environment (number): ")) - 1
            env2_idx = int(input("Select second environment (number): ")) - 1

            if 0 <= env1_idx < len(envs) and 0 <= env2_idx < len(envs):
                diff = self.config_manager.compare_environments(envs[env1_idx], envs[env2_idx])

                print(f"\nComparing {envs[env1_idx]} with {envs[env2_idx]}:")
                if diff['only_in_env1']:
                    print(f"\nOnly in {envs[env1_idx]}:")
                    for var in diff['only_in_env1']:
                        print(f"- {var}")

                if diff['only_in_env2']:
                    print(f"\nOnly in {envs[env2_idx]}:")
                    for var in diff['only_in_env2']:
                        print(f"- {var}")

                if diff['different_values']:
                    print("\nDifferent values:")
                    for var in diff['different_values']:
                        print(f"- {var}")
            else:
                print("\nInvalid selection")
        except ValueError:
            print("\nInvalid input")

    def _show_current_environment(self):
        """Display current environment variables."""
        env_vars = self.config_manager.get_current_environment()
        if env_vars:
            print("\nCurrent environment variables:")
            for key, value in env_vars.items():
                # Mask sensitive values
                if any(s in key.upper() for s in ['KEY', 'SECRET', 'TOKEN', 'PASS']):
                    value = '*' * 8
                print(f"{key}={value}")
        else:
            print("\nNo environment variables found")

    def _show_build_config(self):
        """Display current build configuration."""
        config = self.config_manager.get_build_config()
        if config:
            print("\nCurrent build configuration:")
            for key, value in config.items():
                print(f"{key}: {value}")
        else:
            print("\nNo build configuration found")

    def _set_build_mode(self):
        """Set build mode."""
        print("\nAvailable modes:")
        modes = ['development', 'production', 'staging']
        for i, mode in enumerate(modes, 1):
            print(f"{i}. {mode}")

        try:
            choice = int(input("\nSelect build mode (number): "))
            if 1 <= choice <= len(modes):
                self.config_manager.set_build_mode(modes[choice-1])
            else:
                print("\nInvalid selection")
        except ValueError:
            print("\nInvalid input")

    def _update_build_settings(self):
        """Update build configuration settings."""
        print("\nEnter build settings (empty to skip):")
        updates = {}

        settings = [
            ('optimization', 'Enable optimization (true/false)'),
            ('sourceMaps', 'Generate source maps (true/false)'),
            ('minify', 'Enable minification (true/false)'),
            ('target', 'Build target (e.g., es2015, es2020)'),
        ]

        for key, prompt in settings:
            value = input(f"{prompt}: ").strip()
            if value:
                if value.lower() in ['true', 'false']:
                    updates[key] = value.lower() == 'true'
                else:
                    updates[key] = value

        if updates:
            self.config_manager.update_build_config(updates)
        else:
            print("\nNo updates provided")

    def _configure_host(self):
        """Configure development server host and port."""
        current = self.config_manager.get_host_config()

        host = input(f"\nEnter host (current: {current['host']}): ").strip()
        if not host:
            host = current['host']

        try:
            port = input(f"Enter port (current: {current['port']}): ").strip()
            port = int(port) if port else current['port']

            self.config_manager.configure_host(host, port)
        except ValueError:
            print("\nInvalid port number")

    def _rotate_secrets(self):
        """Rotate sensitive configuration values."""
        confirm = input("\nThis will rotate all secret values. Continue? (y/N): ")
        if confirm.lower() == 'y':
            self.config_manager.rotate_secrets()
        else:
            print("\nSecret rotation cancelled")

    def _show_secret_status(self):
        """Display information about secret configurations."""
        env_vars = self.config_manager.get_current_environment()
        if not env_vars:
            print("\nNo environment variables found")
            return

        secret_vars = [k for k in env_vars.keys()
                      if any(s in k.upper() for s in ['KEY', 'SECRET', 'TOKEN', 'PASS'])]

        if secret_vars:
            print("\nSecret configurations found:")
            for var in secret_vars:
                print(f"- {var}")
            print(f"\nTotal secrets: {len(secret_vars)}")
        else:
            print("\nNo secret configurations found")
