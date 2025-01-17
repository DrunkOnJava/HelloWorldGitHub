"""Git and GitHub operations functionality."""

import os
import json
import subprocess
from typing import Dict, Any, List, Optional
from datetime import datetime

class GitManager:
    """Handles Git and GitHub operations."""
    def __init__(self, ui):
        self.ui = ui
        self.project_root = "/Users/drunkonjava/Desktop/HelloWorldGitHub"

    def get_repo_status(self) -> Dict[str, Any]:
        """Get repository status information."""
        try:
            # Run git commands to get status
            status_cmd = subprocess.run(
                "git status --porcelain",
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True
            )

            branch_cmd = subprocess.run(
                "git branch --show-current",
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True
            )

            remote_cmd = subprocess.run(
                "git remote -v",
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True
            )

            # Parse status output
            changes = status_cmd.stdout.strip().split('\n')
            changes = [c for c in changes if c]

            # Parse remote output
            remotes = {}
            for line in remote_cmd.stdout.strip().split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        remotes[parts[0]] = parts[1]

            return {
                'branch': branch_cmd.stdout.strip(),
                'changes': len(changes),
                'changed_files': changes,
                'remotes': remotes
            }

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to get repo status: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return {}

    def manage_branches(self, action: str, branch_name: str = '') -> bool:
        """Manage Git branches."""
        try:
            if action == 'create':
                if not branch_name:
                    return False
                subprocess.run(
                    f"git checkout -b {branch_name}",
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Created and switched to branch: {branch_name}{self.ui.theme.COLORS['ENDC']}")

            elif action == 'delete':
                if not branch_name:
                    return False
                subprocess.run(
                    f"git branch -D {branch_name}",
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Deleted branch: {branch_name}{self.ui.theme.COLORS['ENDC']}")

            elif action == 'list':
                result = subprocess.run(
                    "git branch",
                    shell=True,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                print("\nAvailable branches:")
                print(result.stdout)

            return True

        except subprocess.CalledProcessError as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Git command failed: {e.stderr}{self.ui.theme.COLORS['ENDC']}")
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to manage branches: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def sync_repository(self) -> bool:
        """Sync with remote repository."""
        try:
            # First fetch
            subprocess.run(
                "git fetch --all",
                shell=True,
                cwd=self.project_root,
                check=True
            )
            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Fetched all remote changes{self.ui.theme.COLORS['ENDC']}")

            # Get current branch
            branch = subprocess.run(
                "git branch --show-current",
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            # Pull changes
            subprocess.run(
                f"git pull origin {branch}",
                shell=True,
                cwd=self.project_root,
                check=True
            )
            print(f"{self.ui.theme.COLORS['SUCCESS']}Pulled latest changes from origin/{branch}{self.ui.theme.COLORS['ENDC']}")

            # Push changes
            subprocess.run(
                f"git push origin {branch}",
                shell=True,
                cwd=self.project_root,
                check=True
            )
            print(f"{self.ui.theme.COLORS['SUCCESS']}Pushed local changes to origin/{branch}{self.ui.theme.COLORS['ENDC']}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Git command failed: {e.stderr}{self.ui.theme.COLORS['ENDC']}")
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to sync repository: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def manage_pull_requests(self, action: str, pr_data: Optional[Dict] = None) -> bool:
        """Manage GitHub pull requests using gh CLI."""
        try:
            if action == 'list':
                result = subprocess.run(
                    "gh pr list",
                    shell=True,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                print("\nCurrent Pull Requests:")
                print(result.stdout)

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

                subprocess.run(
                    cmd,
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Created new PR: {title}{self.ui.theme.COLORS['ENDC']}")

            elif action == 'review' and pr_data:
                number = pr_data.get('number')
                if not number:
                    return False

                # First, show PR diff
                subprocess.run(
                    f"gh pr diff {number}",
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )

                # Then show PR status
                subprocess.run(
                    f"gh pr status {number}",
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )

                # Add review comment if provided
                comment = pr_data.get('comment', '')
                if comment:
                    subprocess.run(
                        f'gh pr review {number} --comment -b "{comment}"',
                        shell=True,
                        cwd=self.project_root,
                        check=True
                    )

            elif action == 'merge' and pr_data:
                number = pr_data.get('number')
                if not number:
                    return False

                method = pr_data.get('method', 'merge')  # merge, squash, or rebase
                cmd = f"gh pr merge {number} --{method}"

                if pr_data.get('delete_branch', True):
                    cmd += " --delete-branch"

                subprocess.run(
                    cmd,
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Merged PR #{number}{self.ui.theme.COLORS['ENDC']}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}GitHub CLI command failed: {e.stderr}{self.ui.theme.COLORS['ENDC']}")
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to manage pull requests: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

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

            # Apply protection rules using gh api
            subprocess.run(
                f'gh api -X PUT /repos/{{owner}}/{{repo}}/branches/{branch}/protection --input {config_path}',
                shell=True,
                cwd=self.project_root,
                check=True
            )

            # Clean up temporary file
            os.remove(config_path)

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Applied branch protection rules to {branch}{self.ui.theme.COLORS['ENDC']}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to set branch protection: {e.stderr}{self.ui.theme.COLORS['ENDC']}")
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to manage branch protection: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

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

                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Created workflow: {filename}{self.ui.theme.COLORS['ENDC']}")

            elif action == 'list':
                result = subprocess.run(
                    "gh workflow list",
                    shell=True,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                print("\nGitHub Actions Workflows:")
                print(result.stdout)

            elif action == 'run' and pipeline_data:
                workflow = pipeline_data.get('workflow')
                if not workflow:
                    return False

                subprocess.run(
                    f"gh workflow run {workflow}",
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Triggered workflow: {workflow}{self.ui.theme.COLORS['ENDC']}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}GitHub CLI command failed: {e.stderr}{self.ui.theme.COLORS['ENDC']}")
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to manage CI pipeline: {str(e)}{self.ui.theme.COLORS['ENDC']}")
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

        return json.dumps(workflow, indent=2)

    def manage_issues(self, action: str, issue_data: Dict = None) -> bool:
        """Manage GitHub issues using gh CLI."""
        try:
            if action == 'list':
                result = subprocess.run(
                    "gh issue list",
                    shell=True,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                print("\nCurrent Issues:")
                print(result.stdout)

            elif action == 'create' and issue_data:
                title = issue_data.get('title', '')
                body = issue_data.get('body', '')
                labels = ','.join(issue_data.get('labels', []))

                cmd = f'gh issue create --title "{title}" --body "{body}"'
                if labels:
                    cmd += f' --label "{labels}"'

                subprocess.run(
                    cmd,
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Created new issue: {title}{self.ui.theme.COLORS['ENDC']}")

            elif action == 'close' and issue_data:
                number = issue_data.get('number')
                if not number:
                    return False

                subprocess.run(
                    f"gh issue close {number}",
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Closed issue #{number}{self.ui.theme.COLORS['ENDC']}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}GitHub CLI command failed: {e.stderr}{self.ui.theme.COLORS['ENDC']}")
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to manage issues: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def manage_secrets(self, action: str, secret_data: Dict = None) -> bool:
        """Manage GitHub Actions secrets using gh CLI."""
        try:
            if action == 'list':
                result = subprocess.run(
                    "gh secret list",
                    shell=True,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                print("\nRepository Secrets:")
                print(result.stdout)

            elif action == 'set' and secret_data:
                name = secret_data.get('name', '')
                value = secret_data.get('value', '')
                if not name or not value:
                    return False

                subprocess.run(
                    f'gh secret set {name}',
                    shell=True,
                    cwd=self.project_root,
                    input=value,
                    text=True,
                    check=True
                )
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Set secret: {name}{self.ui.theme.COLORS['ENDC']}")

            elif action == 'delete' and secret_data:
                name = secret_data.get('name', '')
                if not name:
                    return False

                subprocess.run(
                    f"gh secret delete {name}",
                    shell=True,
                    cwd=self.project_root,
                    check=True
                )
                print(f"\n{self.ui.theme.COLORS['SUCCESS']}Deleted secret: {name}{self.ui.theme.COLORS['ENDC']}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}GitHub CLI command failed: {e.stderr}{self.ui.theme.COLORS['ENDC']}")
            return False
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to manage secrets: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def configure_pages_settings(self) -> bool:
        """Configure GitHub Pages settings."""
        try:
            # Read current workflow file or create new one
            workflow_dir = os.path.join(self.project_root, ".github/workflows")
            os.makedirs(workflow_dir, exist_ok=True)
            workflow_file = os.path.join(workflow_dir, "pages.yml")

            workflow_content = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          branch: gh-pages
          folder: dist
"""

            with open(workflow_file, 'w') as f:
                f.write(workflow_content)

            # Create or update .nojekyll file
            nojekyll_file = os.path.join(self.project_root, ".nojekyll")
            open(nojekyll_file, 'a').close()

            # Update package.json with deployment script
            with open(os.path.join(self.project_root, "package.json"), 'r') as f:
                package_data = json.load(f)

            if 'scripts' not in package_data:
                package_data['scripts'] = {}

            package_data['scripts']['deploy'] = 'npm run build && gh-pages -d dist'

            with open(os.path.join(self.project_root, "package.json"), 'w') as f:
                json.dump(package_data, f, indent=2)

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Successfully configured GitHub Pages{self.ui.theme.COLORS['ENDC']}")
            print("1. GitHub Pages workflow created")
            print("2. .nojekyll file added")
            print("3. Deploy script added to package.json")
            return True

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to configure Pages: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False
