"""GitHub Pull Request management functionality."""

from typing import Dict, Optional
from .utils import execute_git_command, format_error_message, format_success_message

class PullRequestManager:
    """Handles GitHub Pull Request operations."""

    def __init__(self, ui, project_root: str):
        self.ui = ui
        self.project_root = project_root

    def manage_pull_requests(self, action: str, pr_data: Optional[Dict] = None) -> bool:
        """Manage GitHub pull requests using gh CLI."""
        try:
            if action == 'list':
                output, _ = execute_git_command(
                    "gh pr list",
                    self.project_root
                )
                print("\nCurrent Pull Requests:")
                print(output)

            elif action == 'create' and pr_data:
                title = pr_data.get('title', '')
                body = pr_data.get('body', '')
                base = pr_data.get('base', 'main')
                head = pr_data.get('head', '')
                draft = pr_data.get('draft', False)
                reviewers = ','.join(pr_data.get('reviewers', []))

                cmd = f'gh pr create --title "{title}" --body "{body}" --base {base}'
                if head:
                    cmd += f' --head {head}'
                if draft:
                    cmd += ' --draft'
                if reviewers:
                    cmd += f' --reviewer {reviewers}'

                execute_git_command(cmd, self.project_root)
                print(format_success_message(f"Created new PR: {title}", self.ui.theme.COLORS))

            elif action == 'review' and pr_data:
                number = pr_data.get('number')
                if not number:
                    return False

                # First, show PR diff
                execute_git_command(
                    f"gh pr diff {number}",
                    self.project_root
                )

                # Then show PR status
                execute_git_command(
                    f"gh pr status {number}",
                    self.project_root
                )

                # Add review comment if provided
                comment = pr_data.get('comment', '')
                if comment:
                    execute_git_command(
                        f'gh pr review {number} --comment -b "{comment}"',
                        self.project_root
                    )

            elif action == 'merge' and pr_data:
                number = pr_data.get('number')
                if not number:
                    return False

                method = pr_data.get('method', 'merge')  # merge, squash, or rebase
                cmd = f"gh pr merge {number} --{method}"

                if pr_data.get('delete_branch', True):
                    cmd += " --delete-branch"

                execute_git_command(cmd, self.project_root)
                print(format_success_message(f"Merged PR #{number}", self.ui.theme.COLORS))

            return True

        except Exception as e:
            print(format_error_message(f"Failed to manage pull requests: {str(e)}", self.ui.theme.COLORS))
            return False
