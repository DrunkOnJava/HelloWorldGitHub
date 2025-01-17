"""GitHub Branch Protection management functionality."""

import os
import json
from typing import Dict, Any
from .utils import execute_git_command, format_error_message, format_success_message

class BranchProtectionManager:
    """Handles GitHub Branch Protection operations."""

    def __init__(self, ui, project_root: str):
        self.ui = ui
        self.project_root = project_root

    def manage_branch_protection(self, branch: str, rules: Dict[str, Any]) -> bool:
        """Configure branch protection rules using gh CLI."""
        try:
            # Convert Python dict to GitHub API format
            protection_config = {
                "required_status_checks": {
                    "strict": rules.get('strict_status_checks', True),
                    "contexts": rules.get('required_checks', [])
                },
                "enforce_admins": rules.get('enforce_admins', True),
                "required_pull_request_reviews": {
                    "required_approving_review_count": rules.get('required_reviews', 1),
                    "dismiss_stale_reviews": rules.get('dismiss_stale_reviews', True),
                    "require_code_owner_reviews": rules.get('require_code_owner_reviews', False)
                },
                "restrictions": None
            }

            # Write config to temporary file
            config_path = os.path.join(self.project_root, '.github', 'branch-protection.json')
            os.makedirs(os.path.dirname(config_path), exist_ok=True)

            with open(config_path, 'w') as f:
                json.dump(protection_config, f, indent=2)

            try:
                # Apply protection rules using gh api
                execute_git_command(
                    f'gh api -X PUT /repos/{{owner}}/{{repo}}/branches/{branch}/protection --input {config_path}',
                    self.project_root
                )

                print(format_success_message(f"Applied branch protection rules to {branch}", self.ui.theme.COLORS))
                return True

            finally:
                # Clean up temporary file
                if os.path.exists(config_path):
                    os.remove(config_path)

        except Exception as e:
            print(format_error_message(f"Failed to manage branch protection: {str(e)}", self.ui.theme.COLORS))
            return False

    def get_branch_protection(self, branch: str) -> Dict[str, Any]:
        """Get current branch protection rules."""
        try:
            output, _ = execute_git_command(
                f'gh api /repos/{{owner}}/{{repo}}/branches/{branch}/protection',
                self.project_root
            )
            return json.loads(output)
        except Exception as e:
            print(format_error_message(f"Failed to get branch protection rules: {str(e)}", self.ui.theme.COLORS))
            return {}

    def remove_branch_protection(self, branch: str) -> bool:
        """Remove branch protection rules."""
        try:
            execute_git_command(
                f'gh api -X DELETE /repos/{{owner}}/{{repo}}/branches/{branch}/protection',
                self.project_root
            )
            print(format_success_message(f"Removed branch protection rules from {branch}", self.ui.theme.COLORS))
            return True
        except Exception as e:
            print(format_error_message(f"Failed to remove branch protection: {str(e)}", self.ui.theme.COLORS))
            return False
