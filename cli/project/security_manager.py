"""Security management implementation."""

import json
import os
import subprocess
from typing import Dict, List, Optional
from .dependency_manager import DependencyManager
from .git.secrets import SecretsManager

class SecurityManager:
    """Manages security features and configurations."""

    def __init__(self, project_root: str, ui=None):
        """Initialize security manager.

        Args:
            project_root: Root directory of the project
            ui: Optional UI instance for formatting
        """
        self.project_root = project_root
        self.ui = ui
        self.dependency_manager = DependencyManager(project_root)
        self.secrets_manager = SecretsManager(ui, project_root)

    def run_security_scan(self) -> Dict[str, List[Dict]]:
        """Run comprehensive security scan.

        Returns:
            Dict containing scan results by category
        """
        results = {
            'dependencies': self.scan_dependencies(),
            'code': self.scan_code(),
            'secrets': self.scan_secrets(),
            'best_practices': self.check_security_best_practices()
        }
        return results

    def scan_dependencies(self) -> List[Dict]:
        """Scan dependencies for vulnerabilities.

        Returns:
            List of vulnerability reports
        """
        return self.dependency_manager.scan_vulnerabilities()

    def scan_code(self) -> List[Dict]:
        """Perform static code security analysis.

        Returns:
            List of security issues found
        """
        issues = []

        # Run bandit for Python security checks
        try:
            result = subprocess.run(
                ['bandit', '-r', '.', '-f', 'json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if result.stdout:
                bandit_results = json.loads(result.stdout)
                issues.extend(bandit_results.get('results', []))
        except Exception as e:
            print(f"Error running bandit: {str(e)}")

        # Run npm audit for JavaScript security checks
        try:
            result = subprocess.run(
                ['npm', 'audit', '--json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if result.stdout:
                npm_results = json.loads(result.stdout)
                issues.extend(npm_results.get('advisories', {}).values())
        except Exception as e:
            print(f"Error running npm audit: {str(e)}")

        return issues

    def scan_secrets(self) -> List[Dict]:
        """Scan for exposed secrets in code.

        Returns:
            List of potential secret exposures
        """
        try:
            result = subprocess.run(
                ['gitleaks', 'detect', '--no-git', '--format=json'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            if result.stdout:
                return json.loads(result.stdout)
            return []
        except Exception as e:
            print(f"Error scanning for secrets: {str(e)}")
            return []

    def check_security_best_practices(self) -> List[Dict]:
        """Check adherence to security best practices.

        Returns:
            List of security recommendations
        """
        recommendations = []

        # Check for security files
        security_files = [
            '.npmrc',
            '.env.example',
            'SECURITY.md',
            '.gitignore'
        ]

        for file in security_files:
            if not os.path.exists(os.path.join(self.project_root, file)):
                recommendations.append({
                    'type': 'missing_file',
                    'file': file,
                    'recommendation': f'Add {file} with security configurations'
                })

        # Check package.json for security configurations
        try:
            with open(os.path.join(self.project_root, 'package.json')) as f:
                package_data = json.load(f)

            if not package_data.get('engines'):
                recommendations.append({
                    'type': 'package_json',
                    'issue': 'missing_engines',
                    'recommendation': 'Specify node/npm version requirements'
                })

            if not package_data.get('private'):
                recommendations.append({
                    'type': 'package_json',
                    'issue': 'not_private',
                    'recommendation': 'Mark package as private if not intended for npm'
                })
        except Exception as e:
            print(f"Error checking package.json: {str(e)}")

        return recommendations

    def manage_api_keys(self, action: str, key_data: Optional[Dict] = None) -> bool:
        """Manage API keys securely.

        Args:
            action: Action to perform (add/remove/rotate)
            key_data: Optional key data for the action

        Returns:
            bool indicating success
        """
        return self.secrets_manager.manage_secrets(action, key_data)

    def configure_oauth(self, config: Dict) -> bool:
        """Configure OAuth settings.

        Args:
            config: OAuth configuration data

        Returns:
            bool indicating success
        """
        try:
            config_path = os.path.join(self.project_root, '.env')

            # Read existing config
            env_vars = {}
            if os.path.exists(config_path):
                with open(config_path) as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            env_vars[key] = value

            # Update with new OAuth config
            env_vars.update({
                'OAUTH_CLIENT_ID': config.get('client_id', ''),
                'OAUTH_CLIENT_SECRET': config.get('client_secret', ''),
                'OAUTH_REDIRECT_URI': config.get('redirect_uri', ''),
                'OAUTH_SCOPES': ','.join(config.get('scopes', [])),
                'OAUTH_PROVIDER': config.get('provider', '')
            })

            # Write updated config
            with open(config_path, 'w') as f:
                for key, value in env_vars.items():
                    f.write(f'{key}={value}\n')

            return True
        except Exception as e:
            print(f"Error configuring OAuth: {str(e)}")
            return False

    def manage_tokens(self, action: str, token_data: Optional[Dict] = None) -> bool:
        """Manage authentication tokens.

        Args:
            action: Action to perform (create/revoke/refresh)
            token_data: Optional token data for the action

        Returns:
            bool indicating success
        """
        try:
            if action == 'create':
                # Store token securely using secrets manager
                return self.secrets_manager.manage_secrets('set', {
                    'name': token_data.get('name'),
                    'value': token_data.get('token')
                })
            elif action == 'revoke':
                # Remove token from secrets
                return self.secrets_manager.manage_secrets('delete', {
                    'name': token_data.get('name')
                })
            elif action == 'refresh':
                # Implement token refresh logic based on type
                pass
            return False
        except Exception as e:
            print(f"Error managing tokens: {str(e)}")
            return False

    def enforce_security_policies(self) -> bool:
        """Enforce security policies and configurations.

        Returns:
            bool indicating success
        """
        try:
            # Run security scan
            scan_results = self.run_security_scan()

            # Check for critical issues
            critical_issues = []

            # Check dependencies
            if scan_results['dependencies']:
                critical_issues.extend([
                    v for v in scan_results['dependencies']
                    if v.get('severity') == 'critical'
                ])

            # Check code scan
            if scan_results['code']:
                critical_issues.extend([
                    i for i in scan_results['code']
                    if i.get('severity', '').lower() == 'high'
                ])

            # Check secrets
            if scan_results['secrets']:
                critical_issues.extend(scan_results['secrets'])

            # Enforce fixes for critical issues
            if critical_issues:
                # Try to fix vulnerabilities
                self.dependency_manager.fix_vulnerabilities()

                # Report remaining issues
                print("Critical security issues found:")
                for issue in critical_issues:
                    print(f"- {issue.get('title', 'Unknown issue')}")
                return False

            return True
        except Exception as e:
            print(f"Error enforcing security policies: {str(e)}")
            return False
