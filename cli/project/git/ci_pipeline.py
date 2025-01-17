"""GitHub Actions CI/CD pipeline management functionality."""

import os
import json
from typing import Dict, Any, Optional
from .utils import execute_git_command, format_error_message, format_success_message

class CIPipelineManager:
    """Handles GitHub Actions CI/CD pipeline operations."""

    def __init__(self, ui, project_root: str):
        self.ui = ui
        self.project_root = project_root

    def manage_ci_pipeline(self, action: str, pipeline_data: Optional[Dict] = None) -> bool:
        """Manage GitHub Actions CI/CD pipeline."""
        try:
            workflows_dir = os.path.join(self.project_root, '.github', 'workflows')
            os.makedirs(workflows_dir, exist_ok=True)

            if action == 'create' and pipeline_data:
                workflow_name = pipeline_data.get('name', 'CI')
                filename = f"{workflow_name.lower().replace(' ', '-')}.yml"
                filepath = os.path.join(workflows_dir, filename)

                # Generate workflow content
                workflow_content = self._generate_workflow_content(pipeline_data)

                with open(filepath, 'w') as f:
                    f.write(workflow_content)

                print(format_success_message(f"Created workflow: {filename}", self.ui.theme.COLORS))

            elif action == 'list':
                output, _ = execute_git_command(
                    "gh workflow list",
                    self.project_root
                )
                print("\nGitHub Actions Workflows:")
                print(output)

            elif action == 'run' and pipeline_data:
                workflow = pipeline_data.get('workflow')
                if not workflow:
                    return False

                execute_git_command(
                    f"gh workflow run {workflow}",
                    self.project_root
                )
                print(format_success_message(f"Triggered workflow: {workflow}", self.ui.theme.COLORS))

            elif action == 'view-runs' and pipeline_data:
                workflow = pipeline_data.get('workflow')
                if not workflow:
                    return False

                output, _ = execute_git_command(
                    f"gh run list --workflow {workflow}",
                    self.project_root
                )
                print(f"\nWorkflow Runs for {workflow}:")
                print(output)

            return True

        except Exception as e:
            print(format_error_message(f"Failed to manage CI pipeline: {str(e)}", self.ui.theme.COLORS))
            return False

    def _generate_workflow_content(self, pipeline_data: Dict[str, Any]) -> str:
        """Generate GitHub Actions workflow content."""
        workflow = {
            'name': pipeline_data.get('name', 'CI'),
            'on': {
                'push': {
                    'branches': pipeline_data.get('branches', ['main'])
                },
                'pull_request': {
                    'branches': pipeline_data.get('branches', ['main'])
                }
            },
            'jobs': {}
        }

        # Add build job
        if pipeline_data.get('build', True):
            workflow['jobs']['build'] = {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'uses': 'actions/checkout@v3'},
                    {
                        'name': 'Setup Node.js',
                        'uses': 'actions/setup-node@v3',
                        'with': {
                            'node-version': pipeline_data.get('node_version', '18'),
                            'cache': 'npm'
                        }
                    },
                    {
                        'name': 'Install dependencies',
                        'run': 'npm ci'
                    },
                    {
                        'name': 'Build',
                        'run': 'npm run build'
                    }
                ]
            }

        # Add test job
        if pipeline_data.get('test', True):
            workflow['jobs']['test'] = {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'uses': 'actions/checkout@v3'},
                    {
                        'name': 'Setup Node.js',
                        'uses': 'actions/setup-node@v3',
                        'with': {
                            'node-version': pipeline_data.get('node_version', '18'),
                            'cache': 'npm'
                        }
                    },
                    {
                        'name': 'Install dependencies',
                        'run': 'npm ci'
                    },
                    {
                        'name': 'Run tests',
                        'run': 'npm test'
                    }
                ]
            }

        # Add lint job
        if pipeline_data.get('lint', True):
            workflow['jobs']['lint'] = {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'uses': 'actions/checkout@v3'},
                    {
                        'name': 'Setup Node.js',
                        'uses': 'actions/setup-node@v3',
                        'with': {
                            'node-version': pipeline_data.get('node_version', '18'),
                            'cache': 'npm'
                        }
                    },
                    {
                        'name': 'Install dependencies',
                        'run': 'npm ci'
                    },
                    {
                        'name': 'Lint',
                        'run': 'npm run lint'
                    }
                ]
            }

        # Convert to YAML format
        return json.dumps(workflow, indent=2)

    def disable_workflow(self, workflow_name: str) -> bool:
        """Disable a GitHub Actions workflow."""
        try:
            execute_git_command(
                f"gh workflow disable {workflow_name}",
                self.project_root
            )
            print(format_success_message(f"Disabled workflow: {workflow_name}", self.ui.theme.COLORS))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to disable workflow: {str(e)}", self.ui.theme.COLORS))
            return False

    def enable_workflow(self, workflow_name: str) -> bool:
        """Enable a GitHub Actions workflow."""
        try:
            execute_git_command(
                f"gh workflow enable {workflow_name}",
                self.project_root
            )
            print(format_success_message(f"Enabled workflow: {workflow_name}", self.ui.theme.COLORS))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to enable workflow: {str(e)}", self.ui.theme.COLORS))
            return False
