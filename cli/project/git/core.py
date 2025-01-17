"""Core Git operations functionality."""

from typing import Dict, Any, List
from .utils import execute_git_command, format_error_message, format_success_message

class GitCore:
    """Handles core Git operations."""

    def __init__(self, ui, project_root: str):
        self.ui = ui
        self.project_root = project_root

    def get_repo_status(self) -> Dict[str, Any]:
        """Get repository status information."""
        try:
            # Run git commands to get status
            status_output, _ = execute_git_command(
                "git status --porcelain",
                self.project_root
            )

            branch_output, _ = execute_git_command(
                "git branch --show-current",
                self.project_root
            )

            remote_output, _ = execute_git_command(
                "git remote -v",
                self.project_root
            )

            # Parse status output
            changes = status_output.strip().split('\n')
            changes = [c for c in changes if c]

            # Parse remote output
            remotes = {}
            for line in remote_output.strip().split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        remotes[parts[0]] = parts[1]

            return {
                'branch': branch_output.strip(),
                'changes': len(changes),
                'changed_files': changes,
                'remotes': remotes
            }

        except Exception as e:
            print(format_error_message(f"Failed to get repo status: {str(e)}", self.ui.theme.COLORS))
            return {}

    def manage_branches(self, action: str, branch_name: str = '') -> bool:
        """Manage Git branches."""
        try:
            if action == 'create':
                if not branch_name:
                    return False
                execute_git_command(
                    f"git checkout -b {branch_name}",
                    self.project_root
                )
                print(format_success_message(f"Created and switched to branch: {branch_name}", self.ui.theme.COLORS))

            elif action == 'delete':
                if not branch_name:
                    return False
                execute_git_command(
                    f"git branch -D {branch_name}",
                    self.project_root
                )
                print(format_success_message(f"Deleted branch: {branch_name}", self.ui.theme.COLORS))

            elif action == 'list':
                output, _ = execute_git_command(
                    "git branch",
                    self.project_root
                )
                print("\nAvailable branches:")
                print(output)

            return True

        except Exception as e:
            print(format_error_message(f"Failed to manage branches: {str(e)}", self.ui.theme.COLORS))
            return False

    def sync_repository(self) -> bool:
        """Sync with remote repository."""
        try:
            # First fetch
            execute_git_command(
                "git fetch --all",
                self.project_root
            )
            print(format_success_message("Fetched all remote changes", self.ui.theme.COLORS))

            # Get current branch
            branch_output, _ = execute_git_command(
                "git branch --show-current",
                self.project_root
            )
            branch = branch_output.strip()

            # Pull changes
            execute_git_command(
                f"git pull origin {branch}",
                self.project_root
            )
            print(format_success_message(f"Pulled latest changes from origin/{branch}", self.ui.theme.COLORS))

            # Push changes
            execute_git_command(
                f"git push origin {branch}",
                self.project_root
            )
            print(format_success_message(f"Pushed local changes to origin/{branch}", self.ui.theme.COLORS))

            return True

        except Exception as e:
            print(format_error_message(f"Failed to sync repository: {str(e)}", self.ui.theme.COLORS))
            return False
