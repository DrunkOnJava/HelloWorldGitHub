"""Dependency management implementation."""

import json
import subprocess
from typing import Dict, List, Optional


class DependencyManager:
    """Manages project dependencies and updates."""

    def __init__(self, project_root: str):
        """Initialize dependency manager.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root

    def check_updates(self) -> Dict[str, str]:
        """Check for available dependency updates.

        Returns:
            Dict mapping package names to available versions
        """
        try:
            result = subprocess.run(
                ['npm', 'outdated', '--json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if result.returncode != 0 and result.stdout.strip():
                return json.loads(result.stdout)
            return {}
        except Exception as e:
            print(f"Error checking updates: {str(e)}")
            return {}

    def scan_vulnerabilities(self) -> List[Dict]:
        """Scan for security vulnerabilities in dependencies.

        Returns:
            List of vulnerability reports
        """
        try:
            result = subprocess.run(
                ['npm', 'audit', '--json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if result.stdout.strip():
                audit_data = json.loads(result.stdout)
                return audit_data.get('vulnerabilities', [])
            return []
        except Exception as e:
            print(f"Error scanning vulnerabilities: {str(e)}")
            return []

    def update_package(self, package_name: str, version: Optional[str] = None) -> bool:
        """Update a specific package to the specified or latest version.

        Args:
            package_name: Name of the package to update
            version: Optional specific version to install

        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            cmd = ['npm', 'install', f'{package_name}@{version}' if version else package_name]
            result = subprocess.run(cmd, cwd=self.project_root)
            return result.returncode == 0
        except Exception as e:
            print(f"Error updating package: {str(e)}")
            return False

    def get_installed_versions(self) -> Dict[str, str]:
        """Get currently installed package versions.

        Returns:
            Dict mapping package names to installed versions
        """
        try:
            result = subprocess.run(
                ['npm', 'list', '--json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if result.stdout.strip():
                data = json.loads(result.stdout)
                return data.get('dependencies', {})
            return {}
        except Exception as e:
            print(f"Error getting installed versions: {str(e)}")
            return {}

    def fix_vulnerabilities(self) -> bool:
        """Attempt to fix known vulnerabilities.

        Returns:
            bool: True if fixes were applied successfully
        """
        try:
            result = subprocess.run(
                ['npm', 'audit', 'fix'],
                cwd=self.project_root
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error fixing vulnerabilities: {str(e)}")
            return False

    def get_dependency_tree(self) -> Dict:
        """Get full dependency tree.

        Returns:
            Dict containing dependency tree structure
        """
        try:
            result = subprocess.run(
                ['npm', 'list', '--json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if result.stdout.strip():
                return json.loads(result.stdout)
            return {}
        except Exception as e:
            print(f"Error getting dependency tree: {str(e)}")
            return {}
