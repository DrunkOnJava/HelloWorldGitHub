"""Test management functionality."""

import json
import os
import subprocess
import yaml
from typing import List, Dict, Optional
from datetime import datetime

class TestManager:
    """Handles testing operations including integration tests, test data, and reporting."""
    def __init__(self, ui):
        self.ui = ui
        self.project_root = "/Users/drunkonjava/Desktop/HelloWorldGitHub"
        self.test_data_dir = os.path.join(self.project_root, "test/data")
        self.fixtures_dir = os.path.join(self.test_data_dir, "fixtures")
        self.mocks_dir = os.path.join(self.test_data_dir, "mocks")
        self.reports_dir = os.path.join(self.project_root, "test/reports")

        # Create necessary directories
        for directory in [self.test_data_dir, self.fixtures_dir, self.mocks_dir, self.reports_dir]:
            os.makedirs(directory, exist_ok=True)

    def get_testable_components(self) -> List[str]:
        """Get list of components with test files."""
        try:
            components_dir = os.path.join(self.project_root, "src/components")
            test_files = []

            for root, _, files in os.walk(components_dir):
                for file in files:
                    if file.endswith('.test.tsx') or file.endswith('.test.ts'):
                        # Get component name from test file
                        component_name = file.replace('.test.tsx', '').replace('.test.ts', '')
                        # Get relative path from components directory
                        rel_path = os.path.relpath(root, components_dir)
                        if rel_path != '.':
                            component_name = f"{rel_path}/{component_name}"
                        test_files.append(component_name)

            return sorted(test_files)
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to get testable components: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return []

    def run_component_tests(self, component_path: str) -> bool:
        """Run tests for a specific component."""
        try:
            # Convert path to test file path
            if component_path.endswith('.tsx') or component_path.endswith('.ts'):
                test_path = component_path.replace('.tsx', '.test.tsx').replace('.ts', '.test.ts')
            else:
                test_path = f"{component_path}.test.tsx"

            full_path = os.path.join(self.project_root, "src/components", test_path)
            if not os.path.exists(full_path):
                print(f"\n{self.ui.theme.COLORS['ERROR']}Test file not found: {test_path}{self.ui.theme.COLORS['ENDC']}")
                return False

            # Run jest with specific test file
            process = subprocess.Popen(
                f"cd {self.project_root} && npx jest {full_path} --verbose",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Stream output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())

            return process.poll() == 0

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to run component tests: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def debug_e2e_test(self, test_name: str = '') -> bool:
        """Run E2E tests in debug mode."""
        try:
            # Construct debug command
            command = f"cd {self.project_root} && NODE_OPTIONS='--inspect-brk' npx playwright test"
            if test_name:
                command += f" {test_name}"
            command += " --debug"

            print(f"\n{self.ui.theme.COLORS['INFO']}Starting E2E test in debug mode...{self.ui.theme.COLORS['ENDC']}")
            print(f"{self.ui.theme.COLORS['INFO']}Open Chrome DevTools to connect to debugger{self.ui.theme.COLORS['ENDC']}\n")

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Stream output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())

            return process.poll() == 0

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to debug E2E test: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    # Integration Testing Methods
    def run_integration_tests(self, test_type: str = 'all') -> bool:
        """Run integration tests of specified type (api/database/service/all)."""
        try:
            test_command = "cd {} && ".format(self.project_root)

            if test_type == 'api':
                test_command += "npm run test:integration:api"
            elif test_type == 'database':
                test_command += "npm run test:integration:db"
            elif test_type == 'service':
                test_command += "npm run test:integration:service"
            else:
                test_command += "npm run test:integration"

            process = subprocess.Popen(
                test_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())

            return process.poll() == 0

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to run integration tests: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    # Test Data Management Methods
    def generate_test_fixture(self, name: str, schema: Dict) -> bool:
        """Generate a test fixture based on provided schema."""
        try:
            fixture_path = os.path.join(self.fixtures_dir, f"{name}.yaml")
            with open(fixture_path, 'w') as f:
                yaml.dump(schema, f)
            return True
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to generate fixture: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def create_mock_data(self, name: str, data: Dict) -> bool:
        """Create mock data for testing."""
        try:
            mock_path = os.path.join(self.mocks_dir, f"{name}.json")
            with open(mock_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to create mock data: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def seed_test_database(self, fixture_name: Optional[str] = None) -> bool:
        """Seed test database with fixture data."""
        try:
            seed_command = f"cd {self.project_root} && "
            if fixture_name:
                seed_command += f"npm run db:seed -- --fixture {fixture_name}"
            else:
                seed_command += "npm run db:seed"

            process = subprocess.run(seed_command, shell=True, check=True)
            return process.returncode == 0
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to seed database: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    # Test Reporting Methods
    def generate_test_report(self, test_run_id: str) -> bool:
        """Generate detailed test report with trends and analysis."""
        try:
            # Gather test results
            results_file = os.path.join(self.project_root, "test-results.json")
            if not os.path.exists(results_file):
                return False

            with open(results_file, 'r') as f:
                results = json.load(f)

            # Generate report
            report = {
                'timestamp': datetime.now().isoformat(),
                'run_id': test_run_id,
                'summary': {
                    'total': results.get('numTotalTests', 0),
                    'passed': results.get('numPassedTests', 0),
                    'failed': results.get('numFailedTests', 0),
                    'duration': results.get('testDuration', 0)
                },
                'details': results.get('testResults', [])
            }

            # Save report
            report_path = os.path.join(
                self.reports_dir,
                f"test-report-{test_run_id}.json"
            )
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)

            return True
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to generate test report: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def track_test_history(self) -> List[Dict]:
        """Track and analyze historical test data."""
        try:
            history = []
            for report_file in os.listdir(self.reports_dir):
                if report_file.startswith('test-report-') and report_file.endswith('.json'):
                    with open(os.path.join(self.reports_dir, report_file), 'r') as f:
                        report = json.load(f)
                        history.append(report)

            return sorted(history, key=lambda x: x['timestamp'], reverse=True)
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to track test history: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return []

    def analyze_test_trends(self) -> Dict:
        """Analyze test trends and generate insights."""
        try:
            history = self.track_test_history()
            if not history:
                return {}

            trends = {
                'pass_rate': [],
                'duration': [],
                'failure_patterns': {}
            }

            for report in history:
                summary = report['summary']
                total = summary['total']
                if total > 0:
                    pass_rate = (summary['passed'] / total) * 100
                    trends['pass_rate'].append(pass_rate)
                    trends['duration'].append(summary['duration'])

                    # Track failure patterns
                    for test in report['details']:
                        if test.get('status') == 'failed':
                            name = test.get('name', 'unknown')
                            trends['failure_patterns'][name] = trends['failure_patterns'].get(name, 0) + 1

            return trends
        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to analyze trends: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return {}

    def generate_coverage_badge(self) -> bool:
        """Generate coverage badge from coverage report."""
        try:
            # First ensure we have coverage data
            coverage_file = os.path.join(self.project_root, "coverage/coverage-summary.json")
            if not os.path.exists(coverage_file):
                print(f"\n{self.ui.theme.COLORS['WARNING']}No coverage data found. Running coverage first...{self.ui.theme.COLORS['ENDC']}")

                # Run coverage using npm script
                process = subprocess.Popen(
                    f"cd {self.project_root} && npm run test:coverage",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        print(output.strip())

                if process.poll() != 0:
                    return False

            # Read coverage data
            with open(coverage_file, 'r') as f:
                coverage_data = json.load(f)
                total = coverage_data.get('total', {})
                statements = total.get('statements', {}).get('pct', 0)
                branches = total.get('branches', {}).get('pct', 0)
                functions = total.get('functions', {}).get('pct', 0)
                lines = total.get('lines', {}).get('pct', 0)

            # Generate badge using shields.io
            badges_dir = os.path.join(self.project_root, ".github/badges")
            os.makedirs(badges_dir, exist_ok=True)

            # Create individual badges
            metrics = {
                'statements': statements,
                'branches': branches,
                'functions': functions,
                'lines': lines
            }

            for metric, value in metrics.items():
                color = 'red' if value < 60 else 'yellow' if value < 80 else 'brightgreen'
                badge_url = f"https://img.shields.io/badge/coverage%20{metric}-{value}%25-{color}"

                # Download badge
                badge_path = os.path.join(badges_dir, f"coverage-{metric}.svg")
                subprocess.run(['curl', '-o', badge_path, badge_url], check=True)

            print(f"\n{self.ui.theme.COLORS['SUCCESS']}Successfully generated coverage badges in .github/badges/{self.ui.theme.COLORS['ENDC']}")
            return True

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to generate coverage badge: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def run_test_suite(self, test_type: str = 'all') -> bool:
        """Run the test suite with specified type."""
        try:
            command = f"cd {self.project_root} && "

            if test_type == 'unit':
                command += "npm run test"
            elif test_type == 'e2e':
                command += "npx playwright test"
            elif test_type == 'coverage':
                command += "npm run test:coverage"
            else:  # all
                command += "npm run test && npx playwright test"

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Stream output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())

            return process.poll() == 0

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to run test suite: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False

    def watch_tests(self, component_path: str = '') -> bool:
        """Run tests in watch mode."""
        try:
            command = f"cd {self.project_root} && "

            if component_path:
                # Watch specific component tests
                test_path = component_path.replace('.tsx', '.test.tsx').replace('.ts', '.test.ts')
                full_path = os.path.join("src/components", test_path)
                command += f"npx jest {full_path} --watch"
            else:
                # Watch all tests
                command += "npm run test:watch"

            print(f"\n{self.ui.theme.COLORS['INFO']}Starting tests in watch mode...{self.ui.theme.COLORS['ENDC']}")
            print(f"{self.ui.theme.COLORS['INFO']}Press 'q' to quit watch mode{self.ui.theme.COLORS['ENDC']}\n")

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Stream output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())

            return process.poll() == 0

        except Exception as e:
            print(f"\n{self.ui.theme.COLORS['ERROR']}Failed to start watch mode: {str(e)}{self.ui.theme.COLORS['ENDC']}")
            return False
