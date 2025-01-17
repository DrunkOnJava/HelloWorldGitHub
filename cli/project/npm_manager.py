"""NPM and project management functionality."""

import json
import os
import shutil
import subprocess
from typing import Dict, Optional

class NPMManager:
    """Handles NPM-related operations."""
    def __init__(self, ui):
        self.ui = ui
        self.project_root = "/Users/drunkonjava/Desktop/HelloWorldGitHub"
        self._npm_scripts = self._load_npm_scripts()

    def _load_npm_scripts(self) -> Dict[str, str]:
        """Load available npm scripts from package.json."""
        try:
            with open(f"{self.project_root}/package.json", 'r') as f:
                package_data = json.load(f)
                return package_data.get('scripts', {})
        except Exception as e:
            self.ui.status_bar.update(f"Failed to load npm scripts: {str(e)}", 5)
            return {}

    def _map_command(self, command: str) -> Optional[str]:
        """Map menu commands to actual npm scripts."""
        command_map = {
            'dev': 'dev',
            'preview': 'preview',
            'build': 'build',
            'build:dev': 'build',  # Use regular build for dev build
            'build:css': 'build:css',
            'watch:css': 'watch:css',
            'test': 'test',
            'test:watch': 'test:watch',
            'test:coverage': 'test:coverage',
            'clean': None  # Special case, handled separately
        }
        return command_map.get(command)

    def clean_build(self) -> bool:
        """Clean build artifacts and node_modules."""
        try:
            print(f"\n{self.ui.theme.COLORS['INFO']}Starting clean build process...{self.ui.theme.COLORS['ENDC']}")
            print(f"{self.ui.theme.COLORS['INFO']}This may take a few moments...{self.ui.theme.COLORS['ENDC']}\n")

            # Define directories to clean
            dirs_to_clean = [
                'dist',
                '.astro',
                'node_modules'
            ]

            for dir_name in dirs_to_clean:
                path = os.path.join(self.project_root, dir_name)
                if os.path.exists(path):
                    print(f"{self.ui.theme.COLORS['WARNING']}Removing {dir_name}/...{self.ui.theme.COLORS['ENDC']}")
                    shutil.rmtree(path)
                    print(f"{self.ui.theme.COLORS['SUCCESS']}Successfully removed {dir_name}/{self.ui.theme.COLORS['ENDC']}")

            print(f"\n{self.ui.theme.COLORS['INFO']}Installing dependencies...{self.ui.theme.COLORS['ENDC']}")
            process = subprocess.Popen(
                "npm install",
                shell=True,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Stream output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())

            if process.poll() == 0:
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Clean build completed successfully!{self.ui.theme.COLORS['ENDC']}")
                print(f"{self.ui.theme.COLORS['INFO']}Press Enter to continue...{self.ui.theme.COLORS['ENDC']}")
                input()
                return True
            else:
                error = process.stderr.read()
                print(f"\n{self.ui.theme.COLORS['ERROR']}Error during npm install: {error}{self.ui.theme.COLORS['ENDC']}")
                print(f"{self.ui.theme.COLORS['INFO']}Press Enter to continue...{self.ui.theme.COLORS['ENDC']}")
                input()
                return False

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to clean build: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            print(f"{self.ui.theme.COLORS['INFO']}Press Enter to continue...{self.ui.theme.COLORS['ENDC']}")
            input()
            return False

    def run_npm_command(self, command: str) -> bool:
        """Run an npm command with real-time output."""
        # Handle special case for clean command
        if command == 'clean':
            return self.clean_build()

        if command == 'preview':
            if not self.run_npm_command('build'):
                return False

        # Map command to actual npm script
        npm_script = self._map_command(command)
        if not npm_script:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Unknown command: {command}{self.ui.theme.COLORS['ENDC']}")
            print(f"{self.ui.theme.COLORS['INFO']}Press Enter to continue...{self.ui.theme.COLORS['ENDC']}")
            input()
            return False

        # Verify script exists
        if npm_script not in self._npm_scripts:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Script '{npm_script}' not found in package.json{self.ui.theme.COLORS['ENDC']}")
            print(f"{self.ui.theme.COLORS['INFO']}Press Enter to continue...{self.ui.theme.COLORS['ENDC']}")
            input()
            return False

        try:
            print(f"\n{self.ui.theme.COLORS['INFO']}Running {npm_script}...{self.ui.theme.COLORS['ENDC']}")
            print(f"{self.ui.theme.COLORS['INFO']}This may take a few moments...{self.ui.theme.COLORS['ENDC']}\n")

            process = subprocess.Popen(
                ["npm", "run", npm_script],
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate()

            if process.returncode != 0:
                print(f"\n{self.ui.theme.COLORS['ERROR']}Error running {npm_script}:\n{stderr}{self.ui.theme.COLORS['ENDC']}")
                print(f"{self.ui.theme.COLORS['INFO']}Press Enter to continue...{self.ui.theme.COLORS['ENDC']}")
                input()
                return False

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Successfully completed {npm_script}!{self.ui.theme.COLORS['ENDC']}")
            if command == 'preview':
                import re
                match = re.search(r'http:\/\/localhost:\d+', stdout)
                if match:
                    url = match.group(0)
                    print(f"{self.ui.theme.COLORS['INFO']}Preview URL: {url}{self.ui.theme.COLORS['ENDC']}")
                else:
                    print(f"{self.ui.theme.COLORS['WARNING']}Could not automatically find the preview URL. Please check the terminal output.{self.ui.theme.COLORS['ENDC']}")
            print(f"{self.ui.theme.COLORS['INFO']}Press Enter to continue...{self.ui.theme.COLORS['ENDC']}")
            input()
            return True

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to run {npm_script}: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            print(f"{self.ui.theme.COLORS['INFO']}Press Enter to continue...{self.ui.theme.COLORS['ENDC']}")
            input()
            return False

    def get_project_status(self) -> Dict[str, any]:
        """Get current project status and information."""
        try:
            with open(f"{self.project_root}/package.json", 'r') as f:
                package_data = json.load(f)

            return {
                'name': package_data.get('name', 'Unknown'),
                'version': package_data.get('version', 'Unknown'),
                'dependencies': len(package_data.get('dependencies', {})),
                'devDependencies': len(package_data.get('devDependencies', {})),
                'scripts': len(package_data.get('scripts', {}))
            }
        except Exception as e:
            return {
                'error': f"Failed to get project status: {str(e)}"
            }
