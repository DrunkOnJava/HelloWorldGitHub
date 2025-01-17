"""Deployment management functionality."""
import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class DeploymentManager:
    """Manages deployment-related operations including environments, releases, and rollbacks."""

    def __init__(self, project_root: str):
        """Initialize deployment manager.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.deployments_dir = os.path.join(project_root, '.deployments')
        self.ensure_deployment_structure()

    def ensure_deployment_structure(self) -> None:
        """Ensure required deployment directories and files exist."""
        # Create deployment directories
        os.makedirs(self.deployments_dir, exist_ok=True)
        os.makedirs(os.path.join(self.deployments_dir, 'environments'), exist_ok=True)
        os.makedirs(os.path.join(self.deployments_dir, 'releases'), exist_ok=True)
        os.makedirs(os.path.join(self.deployments_dir, 'backups'), exist_ok=True)

        # Initialize environment configs if they don't exist
        for env in ['development', 'staging', 'production']:
            env_file = os.path.join(self.deployments_dir, 'environments', f'{env}.json')
            if not os.path.exists(env_file):
                self.create_environment(env)

    def create_environment(self, name: str, config: Optional[Dict] = None) -> Dict:
        """Create or update an environment configuration.

        Args:
            name: Environment name
            config: Optional environment configuration

        Returns:
            Dict containing the environment configuration
        """
        default_config = {
            'name': name,
            'url': f'https://{name}.example.com',
            'branch': 'main' if name == 'production' else name,
            'auto_deploy': name == 'development',
            'require_approval': name == 'production',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'variables': {},
            'secrets': {},
            'deployment_checks': [
                'lint',
                'test',
                'build'
            ]
        }

        final_config = {**default_config, **(config or {})}
        config_path = os.path.join(self.deployments_dir, 'environments', f'{name}.json')

        with open(config_path, 'w') as f:
            json.dump(final_config, f, indent=2)

        return final_config

    def get_environment(self, name: str) -> Optional[Dict]:
        """Get environment configuration.

        Args:
            name: Environment name

        Returns:
            Environment configuration if it exists
        """
        config_path = os.path.join(self.deployments_dir, 'environments', f'{name}.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return None

    def create_release(self, version: str, changes: List[str]) -> Dict:
        """Create a new release.

        Args:
            version: Release version
            changes: List of changes in this release

        Returns:
            Dict containing release information
        """
        release = {
            'version': version,
            'changes': changes,
            'created_at': datetime.now().isoformat(),
            'git_commit': self._get_current_commit(),
            'artifacts': []
        }

        # Save release info
        release_path = os.path.join(self.deployments_dir, 'releases', f'{version}.json')
        with open(release_path, 'w') as f:
            json.dump(release, f, indent=2)

        # Update changelog
        self._update_changelog(version, changes)

        return release

    def create_backup(self, environment: str) -> str:
        """Create a backup of the current deployment state.

        Args:
            environment: Environment to backup

        Returns:
            Backup ID
        """
        backup_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(self.deployments_dir, 'backups', backup_id)

        # Create backup of deployment files
        os.makedirs(backup_dir)
        self._backup_deployment_files(backup_dir)

        # Save backup metadata
        metadata = {
            'id': backup_id,
            'environment': environment,
            'created_at': datetime.now().isoformat(),
            'git_commit': self._get_current_commit()
        }

        with open(os.path.join(backup_dir, 'metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)

        return backup_id

    def rollback(self, environment: str, backup_id: str) -> bool:
        """Rollback to a previous deployment state.

        Args:
            environment: Environment to rollback
            backup_id: ID of backup to restore

        Returns:
            True if rollback was successful
        """
        backup_dir = os.path.join(self.deployments_dir, 'backups', backup_id)
        if not os.path.exists(backup_dir):
            return False

        # Create new backup before rolling back
        self.create_backup(environment)

        # Restore from backup
        self._restore_from_backup(backup_dir)
        return True

    def bump_version(self, bump_type: str = 'patch') -> str:
        """Bump the project version.

        Args:
            bump_type: Type of version bump (major, minor, or patch)

        Returns:
            New version string
        """
        pkg_file = os.path.join(self.project_root, 'package.json')
        if os.path.exists(pkg_file):
            with open(pkg_file, 'r') as f:
                pkg_data = json.load(f)

            current = pkg_data.get('version', '0.0.0')
            major, minor, patch = map(int, current.split('.'))

            if bump_type == 'major':
                major += 1
                minor = patch = 0
            elif bump_type == 'minor':
                minor += 1
                patch = 0
            else:  # patch
                patch += 1

            new_version = f'{major}.{minor}.{patch}'
            pkg_data['version'] = new_version

            with open(pkg_file, 'w') as f:
                json.dump(pkg_data, f, indent=2)

            return new_version
        return '0.1.0'

    def _get_current_commit(self) -> str:
        """Get current git commit hash."""
        try:
            from .git.utils import get_current_commit
            return get_current_commit()
        except:
            return 'unknown'

    def _update_changelog(self, version: str, changes: List[str]) -> None:
        """Update CHANGELOG.md with new release information."""
        changelog_path = os.path.join(self.project_root, 'CHANGELOG.md')
        today = datetime.now().strftime('%Y-%m-%d')

        new_entry = f"\n## [{version}] - {today}\n\n"
        for change in changes:
            new_entry += f"- {change}\n"

        if os.path.exists(changelog_path):
            with open(changelog_path, 'r') as f:
                content = f.read()
        else:
            content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n"

        # Insert new entry after header
        parts = content.split('\n\n', 1)
        content = f"{parts[0]}\n{new_entry}\n{parts[1] if len(parts) > 1 else ''}"

        with open(changelog_path, 'w') as f:
            f.write(content)

    def _backup_deployment_files(self, backup_dir: str) -> None:
        """Backup deployment-related files."""
        files_to_backup = [
            'package.json',
            'package-lock.json',
            '.env',
            'dist',
            'build'
        ]

        for item in files_to_backup:
            src = os.path.join(self.project_root, item)
            dst = os.path.join(backup_dir, item)

            if os.path.exists(src):
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

    def _restore_from_backup(self, backup_dir: str) -> None:
        """Restore files from backup."""
        for item in os.listdir(backup_dir):
            if item == 'metadata.json':
                continue

            src = os.path.join(backup_dir, item)
            dst = os.path.join(self.project_root, item)

            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)

            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
