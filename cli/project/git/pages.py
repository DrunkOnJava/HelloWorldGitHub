"""GitHub Pages configuration functionality."""

import os
import json
from typing import Dict, Any
from .utils import execute_git_command, format_error_message, format_success_message

class PagesManager:
    """Handles GitHub Pages operations."""

    def __init__(self, ui, project_root: str):
        self.ui = ui
        self.project_root = project_root

    def configure_pages_settings(self) -> bool:
        """Configure GitHub Pages settings."""
        try:
            # Create workflows directory if it doesn't exist
            workflow_dir = os.path.join(self.project_root, ".github/workflows")
            os.makedirs(workflow_dir, exist_ok=True)
            workflow_file = os.path.join(workflow_dir, "pages.yml")

            workflow_content = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          branch: gh-pages
          folder: dist
"""

            with open(workflow_file, 'w') as f:
                f.write(workflow_content)

            # Create or update .nojekyll file
            nojekyll_file = os.path.join(self.project_root, ".nojekyll")
            open(nojekyll_file, 'a').close()

            # Update package.json with deployment script
            package_file = os.path.join(self.project_root, "package.json")
            if os.path.exists(package_file):
                with open(package_file, 'r') as f:
                    package_data = json.load(f)

                if 'scripts' not in package_data:
                    package_data['scripts'] = {}

                package_data['scripts']['deploy'] = 'npm run build && gh-pages -d dist'

                with open(package_file, 'w') as f:
                    json.dump(package_data, f, indent=2)

            print(format_success_message("Successfully configured GitHub Pages", self.ui.theme.COLORS))
            print("1. GitHub Pages workflow created")
            print("2. .nojekyll file added")
            print("3. Deploy script added to package.json")
            return True

        except Exception as e:
            print(format_error_message(f"Failed to configure Pages: {str(e)}", self.ui.theme.COLORS))
            return False

    def get_pages_status(self) -> Dict[str, Any]:
        """Get GitHub Pages deployment status."""
        try:
            output, _ = execute_git_command(
                "gh api repos/{owner}/{repo}/pages",
                self.project_root
            )
            return json.loads(output)
        except Exception as e:
            print(format_error_message(f"Failed to get Pages status: {str(e)}", self.ui.theme.COLORS))
            return {}

    def enable_pages(self, branch: str = 'gh-pages', path: str = '/') -> bool:
        """Enable GitHub Pages for the repository."""
        try:
            execute_git_command(
                f'gh api --method POST repos/{{owner}}/{{repo}}/pages -f branch="{branch}" -f path="{path}"',
                self.project_root
            )
            print(format_success_message(
                f"Enabled GitHub Pages using branch '{branch}' and path '{path}'",
                self.ui.theme.COLORS
            ))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to enable Pages: {str(e)}", self.ui.theme.COLORS))
            return False

    def update_pages_settings(self, branch: str = None, path: str = None) -> bool:
        """Update GitHub Pages settings."""
        try:
            cmd = 'gh api --method PUT repos/{owner}/{repo}/pages'
            if branch:
                cmd += f' -f branch="{branch}"'
            if path:
                cmd += f' -f path="{path}"'

            execute_git_command(cmd, self.project_root)
            settings = []
            if branch:
                settings.append(f"branch: {branch}")
            if path:
                settings.append(f"path: {path}")

            print(format_success_message(
                f"Updated GitHub Pages settings ({', '.join(settings)})",
                self.ui.theme.COLORS
            ))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to update Pages settings: {str(e)}", self.ui.theme.COLORS))
            return False

    def disable_pages(self) -> bool:
        """Disable GitHub Pages for the repository."""
        try:
            execute_git_command(
                "gh api --method DELETE repos/{owner}/{repo}/pages",
                self.project_root
            )
            print(format_success_message("Disabled GitHub Pages", self.ui.theme.COLORS))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to disable Pages: {str(e)}", self.ui.theme.COLORS))
            return False
