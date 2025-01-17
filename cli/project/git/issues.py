"""GitHub Issues management functionality."""

from typing import Dict, Optional
from .utils import execute_git_command, format_error_message, format_success_message

class IssueManager:
    """Handles GitHub Issues operations."""

    def __init__(self, ui, project_root: str):
        self.ui = ui
        self.project_root = project_root

    def manage_issues(self, action: str, issue_data: Optional[Dict] = None) -> bool:
        """Manage GitHub issues using gh CLI."""
        try:
            if action == 'list':
                output, _ = execute_git_command(
                    "gh issue list",
                    self.project_root
                )
                print("\nCurrent Issues:")
                print(output)

            elif action == 'create' and issue_data:
                title = issue_data.get('title', '')
                body = issue_data.get('body', '')
                labels = ','.join(issue_data.get('labels', []))
                assignees = ','.join(issue_data.get('assignees', []))
                milestone = issue_data.get('milestone')

                cmd = f'gh issue create --title "{title}" --body "{body}"'
                if labels:
                    cmd += f' --label "{labels}"'
                if assignees:
                    cmd += f' --assignee "{assignees}"'
                if milestone:
                    cmd += f' --milestone "{milestone}"'

                execute_git_command(cmd, self.project_root)
                print(format_success_message(f"Created new issue: {title}", self.ui.theme.COLORS))

            elif action == 'close' and issue_data:
                number = issue_data.get('number')
                if not number:
                    return False

                comment = issue_data.get('comment', '')
                cmd = f"gh issue close {number}"
                if comment:
                    cmd += f' --comment "{comment}"'

                execute_git_command(cmd, self.project_root)
                print(format_success_message(f"Closed issue #{number}", self.ui.theme.COLORS))

            elif action == 'reopen' and issue_data:
                number = issue_data.get('number')
                if not number:
                    return False

                comment = issue_data.get('comment', '')
                cmd = f"gh issue reopen {number}"
                if comment:
                    cmd += f' --comment "{comment}"'

                execute_git_command(cmd, self.project_root)
                print(format_success_message(f"Reopened issue #{number}", self.ui.theme.COLORS))

            elif action == 'view' and issue_data:
                number = issue_data.get('number')
                if not number:
                    return False

                output, _ = execute_git_command(
                    f"gh issue view {number}",
                    self.project_root
                )
                print(f"\nIssue #{number}:")
                print(output)

            return True

        except Exception as e:
            print(format_error_message(f"Failed to manage issues: {str(e)}", self.ui.theme.COLORS))
            return False

    def add_comment(self, issue_number: int, comment: str) -> bool:
        """Add a comment to an issue."""
        try:
            execute_git_command(
                f'gh issue comment {issue_number} --body "{comment}"',
                self.project_root
            )
            print(format_success_message(f"Added comment to issue #{issue_number}", self.ui.theme.COLORS))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to add comment: {str(e)}", self.ui.theme.COLORS))
            return False

    def edit_issue(self, number: int, updates: Dict[str, str]) -> bool:
        """Edit an existing issue."""
        try:
            cmd = f"gh issue edit {number}"

            if 'title' in updates:
                cmd += f' --title "{updates["title"]}"'
            if 'body' in updates:
                cmd += f' --body "{updates["body"]}"'
            if 'labels' in updates:
                cmd += f' --add-label "{updates["labels"]}"'
            if 'assignees' in updates:
                cmd += f' --add-assignee "{updates["assignees"]}"'
            if 'milestone' in updates:
                cmd += f' --milestone "{updates["milestone"]}"'

            execute_git_command(cmd, self.project_root)
            print(format_success_message(f"Updated issue #{number}", self.ui.theme.COLORS))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to edit issue: {str(e)}", self.ui.theme.COLORS))
            return False
