"""Documentation tools implementation."""

import os
import subprocess
from typing import List, Dict, Optional
import json
import shutil


class DocumentationManager:
    """Manages project documentation generation and maintenance."""

    def __init__(self, project_root: str):
        """Initialize documentation manager.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.docs_dir = os.path.join(project_root, 'docs')
        self._ensure_docs_directory()

    def _ensure_docs_directory(self) -> None:
        """Ensure docs directory exists."""
        os.makedirs(self.docs_dir, exist_ok=True)

    def generate_api_docs(self, output_dir: Optional[str] = None) -> bool:
        """Generate API documentation using TypeDoc.

        Args:
            output_dir: Optional custom output directory

        Returns:
            bool: True if generation successful
        """
        try:
            cmd = [
                'npx', 'typedoc',
                '--out', output_dir or os.path.join(self.docs_dir, 'api'),
                'src'
            ]
            result = subprocess.run(cmd, cwd=self.project_root)
            return result.returncode == 0
        except Exception as e:
            print(f"Error generating API docs: {str(e)}")
            return False

    def generate_component_docs(self, output_dir: Optional[str] = None) -> bool:
        """Generate component documentation using Storybook.

        Args:
            output_dir: Optional custom output directory

        Returns:
            bool: True if generation successful
        """
        try:
            cmd = [
                'npx', 'build-storybook',
                '-o', output_dir or os.path.join(self.docs_dir, 'components')
            ]
            result = subprocess.run(cmd, cwd=self.project_root)
            return result.returncode == 0
        except Exception as e:
            print(f"Error generating component docs: {str(e)}")
            return False

    def manage_markdown_files(self, action: str, file_path: str, content: Optional[str] = None) -> bool:
        """Manage markdown documentation files.

        Args:
            action: Action to perform ('create', 'update', 'delete')
            file_path: Path to the markdown file
            content: Optional content for create/update actions

        Returns:
            bool: True if operation successful
        """
        try:
            full_path = os.path.join(self.docs_dir, file_path)

            if action == 'create' or action == 'update':
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content or '')
                return True
            elif action == 'delete':
                if os.path.exists(full_path):
                    os.remove(full_path)
                return True
            return False
        except Exception as e:
            print(f"Error managing markdown file: {str(e)}")
            return False

    def list_documentation_files(self) -> List[Dict[str, str]]:
        """List all documentation files.

        Returns:
            List of dicts containing file info
        """
        try:
            docs = []
            for root, _, files in os.walk(self.docs_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.docs_dir)
                    docs.append({
                        'path': rel_path,
                        'type': os.path.splitext(file)[1],
                        'size': os.path.getsize(full_path)
                    })
            return docs
        except Exception as e:
            print(f"Error listing documentation files: {str(e)}")
            return []

    def generate_documentation_index(self) -> bool:
        """Generate documentation index page.

        Returns:
            bool: True if generation successful
        """
        try:
            index_content = ["# Project Documentation\n\n"]

            # Add API docs section if exists
            api_dir = os.path.join(self.docs_dir, 'api')
            if os.path.exists(api_dir):
                index_content.append("## API Documentation\n")
                index_content.append("- [API Documentation](api/index.html)\n\n")

            # Add component docs section if exists
            comp_dir = os.path.join(self.docs_dir, 'components')
            if os.path.exists(comp_dir):
                index_content.append("## Component Documentation\n")
                index_content.append("- [Component Documentation](components/index.html)\n\n")

            # Add other markdown files
            index_content.append("## Additional Documentation\n")
            for doc in self.list_documentation_files():
                if doc['type'] == '.md' and 'index.md' not in doc['path']:
                    name = os.path.splitext(doc['path'])[0].replace('/', ' > ')
                    index_content.append(f"- [{name}]({doc['path']})\n")

            return self.manage_markdown_files('create', 'index.md', ''.join(index_content))
        except Exception as e:
            print(f"Error generating documentation index: {str(e)}")
            return False

    def validate_documentation(self) -> List[Dict[str, str]]:
        """Validate documentation files for issues.

        Returns:
            List of validation issues found
        """
        issues = []
        try:
            # Check for broken internal links
            for doc in self.list_documentation_files():
                if doc['type'] == '.md':
                    full_path = os.path.join(self.docs_dir, doc['path'])
                    with open(full_path, 'r') as f:
                        content = f.read()
                        # Basic link validation - could be enhanced
                        for line_num, line in enumerate(content.split('\n'), 1):
                            if '](' in line:
                                link_start = line.find('](') + 2
                                link_end = line.find(')', link_start)
                                if link_end > link_start:
                                    link = line[link_start:link_end]
                                    if not link.startswith(('http', '#', '/')):
                                        target = os.path.join(
                                            os.path.dirname(full_path),
                                            link
                                        )
                                        if not os.path.exists(target):
                                            issues.append({
                                                'file': doc['path'],
                                                'line': line_num,
                                                'issue': f"Broken link: {link}"
                                            })
            return issues
        except Exception as e:
            print(f"Error validating documentation: {str(e)}")
            return []

    def backup_documentation(self, backup_dir: Optional[str] = None) -> bool:
        """Create backup of documentation.

        Args:
            backup_dir: Optional custom backup directory

        Returns:
            bool: True if backup successful
        """
        try:
            timestamp = subprocess.check_output(
                ['date', '+%Y%m%d_%H%M%S']
            ).decode().strip()

            backup_path = backup_dir or os.path.join(
                self.project_root,
                'backups',
                f'docs_backup_{timestamp}'
            )

            shutil.copytree(self.docs_dir, backup_path)
            return True
        except Exception as e:
            print(f"Error backing up documentation: {str(e)}")
            return False
