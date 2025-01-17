"""GitHub Actions secrets management functionality."""

from typing import Dict, Optional
from .utils import execute_git_command, format_error_message, format_success_message

class SecretsManager:
    """Handles GitHub Actions secrets operations."""

    def __init__(self, ui, project_root: str):
        self.ui = ui
        self.project_root = project_root

    def manage_secrets(self, action: str, secret_data: Optional[Dict] = None) -> bool:
        """Manage GitHub Actions secrets using gh CLI."""
        try:
            if action == 'list':
                output, _ = execute_git_command(
                    "gh secret list",
                    self.project_root
                )
                print("\nRepository Secrets:")
                print(output)

            elif action == 'set' and secret_data:
                name = secret_data.get('name', '')
                value = secret_data.get('value', '')
                if not name or not value:
                    return False

                # Use stdin to securely pass the secret value
                execute_git_command(
                    f'gh secret set {name}',
                    self.project_root,
                    input_data=value
                )
                print(format_success_message(f"Set secret: {name}", self.ui.theme.COLORS))

            elif action == 'delete' and secret_data:
                name = secret_data.get('name', '')
                if not name:
                    return False

                execute_git_command(
                    f"gh secret delete {name}",
                    self.project_root
                )
                print(format_success_message(f"Deleted secret: {name}", self.ui.theme.COLORS))

            elif action == 'sync' and secret_data:
                source_repo = secret_data.get('source_repo', '')
                secrets = secret_data.get('secrets', [])
                if not source_repo or not secrets:
                    return False

                for secret in secrets:
                    execute_git_command(
                        f"gh secret sync {secret} --source-repo {source_repo}",
                        self.project_root
                    )
                print(format_success_message(f"Synced secrets from {source_repo}", self.ui.theme.COLORS))

            return True

        except Exception as e:
            print(format_error_message(f"Failed to manage secrets: {str(e)}", self.ui.theme.COLORS))
            return False

    def set_environment_secret(self, environment: str, name: str, value: str) -> bool:
        """Set a secret for a specific GitHub Environment."""
        try:
            execute_git_command(
                f'gh secret set {name} --env {environment}',
                self.project_root,
                input_data=value
            )
            print(format_success_message(
                f"Set secret '{name}' for environment '{environment}'",
                self.ui.theme.COLORS
            ))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to set environment secret: {str(e)}", self.ui.theme.COLORS))
            return False

    def list_environment_secrets(self, environment: str) -> bool:
        """List secrets for a specific GitHub Environment."""
        try:
            output, _ = execute_git_command(
                f"gh secret list --env {environment}",
                self.project_root
            )
            print(f"\nSecrets for environment '{environment}':")
            print(output)
            return True
        except Exception as e:
            print(format_error_message(f"Failed to list environment secrets: {str(e)}", self.ui.theme.COLORS))
            return False

    def delete_environment_secret(self, environment: str, name: str) -> bool:
        """Delete a secret from a specific GitHub Environment."""
        try:
            execute_git_command(
                f"gh secret delete {name} --env {environment}",
                self.project_root
            )
            print(format_success_message(
                f"Deleted secret '{name}' from environment '{environment}'",
                self.ui.theme.COLORS
            ))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to delete environment secret: {str(e)}", self.ui.theme.COLORS))
            return False
