"""Configuration management functionality."""

import json
import os
import re
import shutil
import secrets
from datetime import datetime
from typing import Dict, Any, List, Optional

class ConfigManager:
    """Handles configuration operations including environment management, build configuration,
    and secret rotation."""
    def __init__(self, ui):
        self.ui = ui
        self.project_root = "/Users/drunkonjava/Desktop/HelloWorldGitHub"
        self.env_path = os.path.join(self.project_root, ".env")
        self.env_backup_dir = os.path.join(self.project_root, ".env-backups")
        self.build_config_path = os.path.join(self.project_root, "build.config.json")

        # Ensure backup directory exists
        os.makedirs(self.env_backup_dir, exist_ok=True)

    def get_environments(self) -> List[str]:
        """Get list of available environment configurations."""
        envs = []
        if os.path.exists(self.env_backup_dir):
            for f in os.listdir(self.env_backup_dir):
                if f.startswith('.env.'):
                    envs.append(f.replace('.env.', ''))
        return envs

    def get_current_environment(self) -> Dict[str, str]:
        """Get current environment variables."""
        env_vars = {}
        if os.path.exists(self.env_path):
            with open(self.env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        return env_vars

    def save_environment(self, name: str) -> bool:
        """Save current environment configuration."""
        try:
            if os.path.exists(self.env_path):
                backup_path = os.path.join(self.env_backup_dir, f'.env.{name}')
                shutil.copy2(self.env_path, backup_path)
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Environment saved as '{name}'{self.ui.theme.COLORS['ENDC']}")
                return True
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to save environment: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def load_environment(self, name: str) -> bool:
        """Load a saved environment configuration."""
        try:
            env_file = os.path.join(self.env_backup_dir, f'.env.{name}')
            if os.path.exists(env_file):
                shutil.copy2(env_file, self.env_path)
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Loaded environment '{name}'{self.ui.theme.COLORS['ENDC']}")
                return True
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to load environment: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def compare_environments(self, env1: str, env2: str) -> Dict[str, Any]:
        """Compare two environment configurations."""
        try:
            env1_path = os.path.join(self.env_backup_dir, f'.env.{env1}')
            env2_path = os.path.join(self.env_backup_dir, f'.env.{env2}')

            env1_vars = {}
            env2_vars = {}

            if os.path.exists(env1_path):
                with open(env1_path, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            env1_vars[key] = value

            if os.path.exists(env2_path):
                with open(env2_path, 'r') as f:
                    for line in f:
                        if '=' in line and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            env2_vars[key] = value

            return {
                'only_in_env1': [k for k in env1_vars if k not in env2_vars],
                'only_in_env2': [k for k in env2_vars if k not in env1_vars],
                'different_values': [k for k in env1_vars if k in env2_vars and env1_vars[k] != env2_vars[k]]
            }
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to compare environments: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return {}

    def rotate_secrets(self) -> bool:
        """Rotate sensitive configuration values."""
        try:
            if not os.path.exists(self.env_path):
                return False

            # Create backup before rotation
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(self.env_backup_dir, f'.env.backup_{timestamp}')
            shutil.copy2(self.env_path, backup_path)

            with open(self.env_path, 'r') as f:
                lines = f.readlines()

            # Identify and rotate secrets
            rotated = False
            for i, line in enumerate(lines):
                if ('KEY' in line or 'SECRET' in line or 'TOKEN' in line) and '=' in line:
                    key, _ = line.strip().split('=', 1)
                    new_secret = secrets.token_urlsafe(32)
                    lines[i] = f"{key}={new_secret}\n"
                    rotated = True

            if rotated:
                with open(self.env_path, 'w') as f:
                    f.writelines(lines)
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Secrets rotated successfully{self.ui.theme.COLORS['ENDC']}")
                return True
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to rotate secrets: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def get_build_config(self) -> Dict[str, Any]:
        """Get current build configuration."""
        try:
            if os.path.exists(self.build_config_path):
                with open(self.build_config_path, 'r') as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}

    def update_build_config(self, updates: Dict[str, Any]) -> bool:
        """Update build configuration."""
        try:
            config = self.get_build_config()
            config.update(updates)

            with open(self.build_config_path, 'w') as f:
                json.dump(config, f, indent=2)

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Build configuration updated{self.ui.theme.COLORS['ENDC']}")
            return True
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to update build configuration: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def set_build_mode(self, mode: str) -> bool:
        """Set build mode (development, production, staging)."""
        try:
            valid_modes = ['development', 'production', 'staging']
            if mode not in valid_modes:
                print(f"\n{self.ui.theme.COLORS['ERROR']}Invalid build mode. Must be one of: {', '.join(valid_modes)}{self.ui.theme.COLORS['ENDC']}")
                return False

            return self.update_build_config({'mode': mode})
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to set build mode: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def configure_host(self, host: str, port: int) -> bool:
        """Configure development server host and port."""
        try:
            # Read astro.config.mjs
            config_path = os.path.join(self.project_root, "astro.config.mjs")
            with open(config_path, 'r') as f:
                content = f.read()

            # Find server configuration section
            server_start = content.find('server:')
            if server_start == -1:
                # No server config exists, add it
                import_end = content.find(';', content.find('defineConfig'))
                if import_end == -1:
                    return False

                # Add server configuration after defineConfig
                updated_content = (
                    content[:import_end+1] +
                    f'\n\nexport default defineConfig({{\n' +
                    f'  server: {{\n' +
                    f'    host: "{host}",\n' +
                    f'    port: {port}\n' +
                    f'  }}\n' +
                    f'}});'
                )
            else:
                # Update existing server config
                config_end = content.find('}', server_start)
                if config_end == -1:
                    return False

                # Extract the part before server config
                before_server = content[:server_start]
                # Find the end of the entire config object
                after_config = content[content.find('}', config_end+1):]

                # Create new server config
                updated_content = (
                    before_server +
                    f'server: {{\n' +
                    f'    host: "{host}",\n' +
                    f'    port: {port}\n' +
                    f'  }}' +
                    after_config
                )

            # Write updated configuration
            with open(config_path, 'w') as f:
                f.write(updated_content)

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Successfully updated host configuration{self.ui.theme.COLORS['ENDC']}")
            print(f"Host: {host}")
            print(f"Port: {port}")
            return True

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to configure host: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def get_host_config(self) -> Dict[str, Any]:
        """Get current host configuration."""
        try:
            config_path = os.path.join(self.project_root, "astro.config.mjs")
            with open(config_path, 'r') as f:
                content = f.read()

            # Try to find host and port in server config
            host_match = re.search(r'host:\s*[\'"]([^\'"]+)[\'"]', content)
            port_match = re.search(r'port:\s*(\d+)', content)

            return {
                'host': host_match.group(1) if host_match else 'localhost',
                'port': int(port_match.group(1)) if port_match else 3000
            }

        except Exception:
            # Return defaults if config can't be read
            return {
                'host': 'localhost',
                'port': 3000
            }

    def update_package_json(self, updates: Dict[str, Any]) -> bool:
        """Update package.json with provided updates."""
        try:
            package_path = os.path.join(self.project_root, "package.json")
            with open(package_path, 'r') as f:
                package_data = json.load(f)

            # Apply updates
            for key, value in updates.items():
                if isinstance(value, dict) and key in package_data:
                    # Merge dictionaries for nested objects
                    package_data[key].update(value)
                else:
                    # Direct assignment for other values
                    package_data[key] = value

            # Write updated package.json
            with open(package_path, 'w') as f:
                json.dump(package_data, f, indent=2)

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Successfully updated package.json{self.ui.theme.COLORS['ENDC']}")
            return True

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to update package.json: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def get_config(self, config_name: str) -> Dict[str, Any]:
        """Get configuration by name."""
        try:
            config_map = {
                'astro': 'astro.config.mjs',
                'package': 'package.json',
                'tsconfig': 'tsconfig.json',
                'prettier': '.prettierrc',
                'eslint': 'eslint.config.mjs'
            }

            if config_name not in config_map:
                return {}

            config_path = os.path.join(self.project_root, config_map[config_name])
            if not os.path.exists(config_path):
                return {}

            with open(config_path, 'r') as f:
                if config_name == 'package' or config_name == 'prettier':
                    return json.load(f)
                else:
                    # For non-JSON files, return the content as a string
                    return {'content': f.read()}

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to get config: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return {}
