"""Git management package."""

from .core import GitCore
from .pull_requests import PullRequestManager
from .branch_protection import BranchProtectionManager
from .ci_pipeline import CIPipelineManager
from .issues import IssueManager
from .secrets import SecretsManager
from .pages import PagesManager
from .utils import GitCommandError, execute_git_command

class GitManager:
    """Main Git management class that coordinates all Git-related operations."""

    def __init__(self, ui):
        self.ui = ui
        self.project_root = "/Users/drunkonjava/Desktop/HelloWorldGitHub"

        # Initialize all managers
        self.core = GitCore(ui, self.project_root)
        self.pull_requests = PullRequestManager(ui, self.project_root)
        self.branch_protection = BranchProtectionManager(ui, self.project_root)
        self.ci_pipeline = CIPipelineManager(ui, self.project_root)
        self.issues = IssueManager(ui, self.project_root)
        self.secrets = SecretsManager(ui, self.project_root)
        self.pages = PagesManager(ui, self.project_root)

    # Delegate methods to appropriate managers
    def get_repo_status(self):
        """Get repository status information."""
        return self.core.get_repo_status()

    def manage_branches(self, action: str, branch_name: str = ''):
        """Manage Git branches."""
        return self.core.manage_branches(action, branch_name)

    def sync_repository(self):
        """Sync with remote repository."""
        return self.core.sync_repository()

    def manage_pull_requests(self, action: str, pr_data=None):
        """Manage GitHub pull requests."""
        return self.pull_requests.manage_pull_requests(action, pr_data)

    def manage_branch_protection(self, branch: str, rules):
        """Configure branch protection rules."""
        return self.branch_protection.manage_branch_protection(branch, rules)

    def manage_ci_pipeline(self, action: str, pipeline_data=None):
        """Manage GitHub Actions CI/CD pipeline."""
        return self.ci_pipeline.manage_ci_pipeline(action, pipeline_data)

    def manage_issues(self, action: str, issue_data=None):
        """Manage GitHub issues."""
        return self.issues.manage_issues(action, issue_data)

    def manage_secrets(self, action: str, secret_data=None):
        """Manage GitHub Actions secrets."""
        return self.secrets.manage_secrets(action, secret_data)

    def configure_pages_settings(self):
        """Configure GitHub Pages settings."""
        return self.pages.configure_pages_settings()
