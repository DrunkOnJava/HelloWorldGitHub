"""Security menu implementation."""

from typing import Dict, Optional
from ..models.menu_item import MenuItem
from ..project.security_manager import SecurityManager

class SecurityMenu:
    """Handles security-related menu options."""

    def __init__(self, ui, project_manager):
        """Initialize security menu.

        Args:
            ui: UI instance for formatting
            project_manager: Project manager instance
        """
        self.ui = ui
        self.project_manager = project_manager
        self.security_manager = SecurityManager(project_manager.project_root, ui)

    def get_menu_items(self) -> Dict[str, MenuItem]:
        """Get security menu items.

        Returns:
            Dict of menu items
        """
        return {
            'scan': MenuItem(
                'Run Security Scan',
                'Perform comprehensive security analysis',
                self.run_security_scan
            ),
            'dependencies': MenuItem(
                'Check Dependencies',
                'Scan dependencies for vulnerabilities',
                self.check_dependencies
            ),
            'code': MenuItem(
                'Analyze Code',
                'Perform static code security analysis',
                self.analyze_code
            ),
            'secrets': MenuItem(
                'Scan Secrets',
                'Check for exposed secrets in code',
                self.scan_secrets
            ),
            'best-practices': MenuItem(
                'Best Practices',
                'Check security best practices compliance',
                self.check_best_practices
            ),
            'api-keys': MenuItem(
                'API Keys',
                'Manage API keys securely',
                self.manage_api_keys
            ),
            'oauth': MenuItem(
                'OAuth',
                'Configure OAuth settings',
                self.configure_oauth
            ),
            'tokens': MenuItem(
                'Tokens',
                'Manage authentication tokens',
                self.manage_tokens
            ),
            'enforce': MenuItem(
                'Enforce Policies',
                'Enforce security policies and configurations',
                self.enforce_policies
            )
        }

    def run_security_scan(self) -> None:
        """Run comprehensive security scan."""
        print("\nRunning comprehensive security scan...")
        results = self.security_manager.run_security_scan()

        # Display results by category
        categories = {
            'dependencies': 'Dependency Vulnerabilities',
            'code': 'Code Security Issues',
            'secrets': 'Exposed Secrets',
            'best_practices': 'Best Practice Recommendations'
        }

        for category, title in categories.items():
            issues = results.get(category, [])
            if issues:
                print(f"\n{title}:")
                for issue in issues:
                    print(f"- {issue.get('title', issue)}")
            else:
                print(f"\n{title}: No issues found")

    def check_dependencies(self) -> None:
        """Check dependencies for vulnerabilities."""
        print("\nScanning dependencies for vulnerabilities...")
        vulnerabilities = self.security_manager.scan_dependencies()

        if vulnerabilities:
            print("\nVulnerabilities found:")
            for vuln in vulnerabilities:
                print(f"- {vuln.get('title')}: {vuln.get('severity')} severity")
                print(f"  {vuln.get('overview')}")
        else:
            print("No vulnerabilities found in dependencies.")

    def analyze_code(self) -> None:
        """Perform code security analysis."""
        print("\nAnalyzing code for security issues...")
        issues = self.security_manager.scan_code()

        if issues:
            print("\nSecurity issues found:")
            for issue in issues:
                print(f"- {issue.get('title')}")
                print(f"  Severity: {issue.get('severity')}")
                print(f"  Location: {issue.get('location', 'Unknown')}")
        else:
            print("No security issues found in code analysis.")

    def scan_secrets(self) -> None:
        """Scan for exposed secrets."""
        print("\nScanning for exposed secrets...")
        secrets = self.security_manager.scan_secrets()

        if secrets:
            print("\nPotential secrets found:")
            for secret in secrets:
                print(f"- {secret.get('description')}")
                print(f"  File: {secret.get('file')}")
                print(f"  Line: {secret.get('line')}")
        else:
            print("No exposed secrets found.")

    def check_best_practices(self) -> None:
        """Check security best practices."""
        print("\nChecking security best practices...")
        recommendations = self.security_manager.check_security_best_practices()

        if recommendations:
            print("\nRecommendations:")
            for rec in recommendations:
                print(f"- {rec.get('recommendation')}")
        else:
            print("All security best practices are being followed.")

    def manage_api_keys(self) -> None:
        """Manage API keys."""
        actions = {
            '1': ('Add', 'add'),
            '2': ('Remove', 'remove'),
            '3': ('Rotate', 'rotate')
        }

        print("\nAPI Key Management:")
        for key, (name, _) in actions.items():
            print(f"{key}. {name}")

        choice = input("\nSelect action (or press Enter to cancel): ")
        if choice in actions:
            _, action = actions[choice]

            if action == 'add':
                name = input("Enter key name: ")
                value = input("Enter key value: ")
                if self.security_manager.manage_api_keys('set', {'name': name, 'value': value}):
                    print("API key added successfully.")

            elif action == 'remove':
                name = input("Enter key name to remove: ")
                if self.security_manager.manage_api_keys('delete', {'name': name}):
                    print("API key removed successfully.")

            elif action == 'rotate':
                name = input("Enter key name to rotate: ")
                new_value = input("Enter new key value: ")
                if self.security_manager.manage_api_keys('set', {'name': name, 'value': new_value}):
                    print("API key rotated successfully.")

    def configure_oauth(self) -> None:
        """Configure OAuth settings."""
        print("\nOAuth Configuration:")
        config = {
            'client_id': input("Enter client ID: "),
            'client_secret': input("Enter client secret: "),
            'redirect_uri': input("Enter redirect URI: "),
            'scopes': input("Enter scopes (comma-separated): ").split(','),
            'provider': input("Enter OAuth provider: ")
        }

        if self.security_manager.configure_oauth(config):
            print("OAuth configured successfully.")
        else:
            print("Failed to configure OAuth.")

    def manage_tokens(self) -> None:
        """Manage authentication tokens."""
        actions = {
            '1': ('Create', 'create'),
            '2': ('Revoke', 'revoke'),
            '3': ('Refresh', 'refresh')
        }

        print("\nToken Management:")
        for key, (name, _) in actions.items():
            print(f"{key}. {name}")

        choice = input("\nSelect action (or press Enter to cancel): ")
        if choice in actions:
            _, action = actions[choice]

            if action == 'create':
                name = input("Enter token name: ")
                token = input("Enter token value: ")
                if self.security_manager.manage_tokens('create', {'name': name, 'token': token}):
                    print("Token created successfully.")

            elif action == 'revoke':
                name = input("Enter token name to revoke: ")
                if self.security_manager.manage_tokens('revoke', {'name': name}):
                    print("Token revoked successfully.")

            elif action == 'refresh':
                name = input("Enter token name to refresh: ")
                if self.security_manager.manage_tokens('refresh', {'name': name}):
                    print("Token refreshed successfully.")

    def enforce_policies(self) -> None:
        """Enforce security policies."""
        print("\nEnforcing security policies...")
        if self.security_manager.enforce_security_policies():
            print("All security policies enforced successfully.")
        else:
            print("Some security policies could not be enforced. See above for details.")
