"""Testing menu implementation."""

import json
from datetime import datetime
from ..models.menu_item import MenuItem

def show_testing_menu(ui) -> None:
    """Testing menu implementation with submenus."""
    while True:
        ui.print_header(
            "Testing",
            "Test Runner and Coverage"
        )

        menu_items = [
            MenuItem(
                key='unit',
                label='Unit Testing',
                description='Component and unit test options',
                icon='🧪',
                shortcut='u'
            ),
            MenuItem(
                key='integration',
                label='Integration Tests',
                description='Run API, database and service tests',
                icon='🔄',
                shortcut='i'
            ),
            MenuItem(
                key='e2e',
                label='E2E Testing',
                description='End-to-end testing options',
                icon='🔄',
                shortcut='e'
            ),
            MenuItem(
                key='test_data',
                label='Test Data',
                description='Manage fixtures, mocks and seeding',
                icon='📦',
                shortcut='d'
            ),
            MenuItem(
                key='coverage',
                label='Coverage Options',
                description='Test coverage and reporting',
                icon='📊',
                shortcut='c'
            ),
            MenuItem(
                key='performance',
                label='Performance Testing',
                description='Run performance and load tests',
                icon='⚡',
                shortcut='p'
            ),
            MenuItem(
                key='mocking',
                label='API Mocking',
                description='Configure and manage API mocks',
                icon='🔌',
                shortcut='m'
            ),
            MenuItem(
                key='reporting',
                label='Test Reports',
                description='View and analyze test results',
                icon='📋',
                shortcut='r'
            ),
            MenuItem(
                key='snapshot',
                label='Snapshot Tests',
                description='Manage component snapshots',
                icon='📸',
                shortcut='s'
            ),
            MenuItem(
                key='back',
                label='Back to Main Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'unit':
            show_unit_testing_submenu(ui)
        elif choice == 'e2e':
            show_e2e_testing_submenu(ui)
        elif choice == 'coverage':
            show_coverage_submenu(ui)
        elif choice == 'performance':
            show_performance_submenu(ui)
        elif choice == 'mocking':
            show_mocking_submenu(ui)
        elif choice == 'integration':
            show_integration_submenu(ui)
        elif choice == 'test_data':
            show_test_data_submenu(ui)
        elif choice == 'reporting':
            show_reporting_submenu(ui)
        elif choice == 'snapshot':
            show_snapshot_submenu(ui)

def show_unit_testing_submenu(ui) -> None:
    """Unit testing submenu."""
    while True:
        ui.print_header(
            "Unit Testing",
            "Component and Unit Tests"
        )

        menu_items = [
            MenuItem(
                key='test',
                label='Run All Tests',
                description='Execute all unit tests',
                icon='✓',
                shortcut='t'
            ),
            MenuItem(
                key='watch',
                label='Watch Tests',
                description='Run tests in watch mode',
                icon='👁️',
                shortcut='w'
            ),
            MenuItem(
                key='components',
                label='Test Components',
                description='Run component-specific tests',
                icon='🧩',
                shortcut='c'
            ),
            MenuItem(
                key='back',
                label='Back to Testing Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'test':
            ui.project.run_npm_command('test')
        elif choice == 'watch':
            ui.project.run_npm_command('test:watch')
        elif choice == 'components':
            run_component_tests(ui)

def run_component_tests(ui) -> None:
    """Run tests for specific components."""
    ui.print_header(
        "Component Tests",
        "Run Tests for Specific Components"
    )

    # Get list of testable components
    components = ui.project.get_testable_components()
    if not components:
        ui.status_bar.update("No testable components found", 3)
        return

    # Display component list
    print("\nAvailable Components:")
    for i, component in enumerate(components, 1):
        print(f"{i}. {component}")

    try:
        selection = int(ui.get_input("\nSelect component number (or 0 for all)", required=True))
        if selection == 0:
            if ui.project.run_test_suite('components'):
                ui.status_bar.update("Successfully ran all component tests", 3)
            else:
                ui.status_bar.update("Component tests failed", 3)
        elif selection > 0 and selection <= len(components):
            component = components[selection-1]
            if ui.project.run_component_tests(component):
                ui.status_bar.update(f"Successfully ran tests for {component}", 3)
            else:
                ui.status_bar.update(f"Tests failed for {component}", 3)
        else:
            ui.status_bar.update("Invalid selection", 3)
    except ValueError:
        ui.status_bar.update("Invalid input", 3)

def show_e2e_testing_submenu(ui) -> None:
    """E2E testing submenu."""
    while True:
        ui.print_header(
            "E2E Testing",
            "End-to-End Tests"
        )

        menu_items = [
            MenuItem(
                key='e2e',
                label='Run E2E Tests',
                description='Execute all E2E tests',
                icon='🔄',
                shortcut='e'
            ),
            MenuItem(
                key='e2e_watch',
                label='Watch E2E Tests',
                description='Run E2E tests in watch mode',
                icon='👁️',
                shortcut='w'
            ),
            MenuItem(
                key='e2e_debug',
                label='Debug E2E Tests',
                description='Run E2E tests with debugging',
                icon='🔍',
                shortcut='d'
            ),
            MenuItem(
                key='back',
                label='Back to Testing Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'e2e':
            ui.project.run_npm_command('test:e2e')
        elif choice == 'e2e_watch':
            ui.project.run_npm_command('test:e2e:watch')
        elif choice == 'e2e_debug':
            debug_e2e_tests(ui)

def debug_e2e_tests(ui) -> None:
    """Debug E2E tests with Chrome DevTools."""
    ui.print_header(
        "Debug E2E Tests",
        "Run E2E Tests in Debug Mode"
    )

    # Get list of E2E tests
    tests = ui.project.get_e2e_tests()
    if not tests:
        ui.status_bar.update("No E2E tests found", 3)
        return

    # Display test list
    print("\nAvailable E2E Tests:")
    print("0. All Tests")
    for i, test in enumerate(tests, 1):
        print(f"{i}. {test}")

    try:
        selection = int(ui.get_input("\nSelect test number", required=True))
        if selection == 0:
            if ui.project.debug_e2e_test():
                ui.status_bar.update("E2E debugging session completed", 3)
            else:
                ui.status_bar.update("E2E debugging session failed", 3)
        elif selection > 0 and selection <= len(tests):
            test = tests[selection-1]
            if ui.project.debug_e2e_test(test):
                ui.status_bar.update(f"Successfully debugged test: {test}", 3)
            else:
                ui.status_bar.update(f"Failed to debug test: {test}", 3)
        else:
            ui.status_bar.update("Invalid selection", 3)
    except ValueError:
        ui.status_bar.update("Invalid input", 3)

def show_coverage_submenu(ui) -> None:
    """Coverage options submenu."""
    while True:
        ui.print_header(
            "Coverage Options",
            "Test Coverage and Reporting"
        )

        menu_items = [
            MenuItem(
                key='coverage',
                label='Generate Coverage',
                description='Generate test coverage report',
                icon='📊',
                shortcut='c'
            ),
            MenuItem(
                key='coverage_html',
                label='HTML Report',
                description='Generate HTML coverage report',
                icon='📱',
                shortcut='h'
            ),
            MenuItem(
                key='coverage_badges',
                label='Coverage Badges',
                description='Generate coverage badges',
                icon='🏷️',
                shortcut='b'
            ),
            MenuItem(
                key='back',
                label='Back to Testing Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'coverage':
            ui.project.run_npm_command('test:coverage')
        elif choice == 'coverage_html':
            ui.project.run_npm_command('test:coverage:html')
        elif choice == 'coverage_badges':
            if ui.project.generate_coverage_badge():
                ui.status_bar.update("Successfully generated coverage badges", 3)
            else:
                ui.status_bar.update("Failed to generate coverage badges", 3)

def show_performance_submenu(ui) -> None:
    """Performance testing submenu."""
    while True:
        ui.print_header(
            "Performance Testing",
            "Performance and Load Testing"
        )

        menu_items = [
            MenuItem(
                key='lighthouse',
                label='Lighthouse Audit',
                description='Run Lighthouse performance audit',
                icon='🏠',
                shortcut='l'
            ),
            MenuItem(
                key='load',
                label='Load Testing',
                description='Run k6 load tests',
                icon='⚡',
                shortcut='k'
            ),
            MenuItem(
                key='bundle',
                label='Bundle Analysis',
                description='Analyze bundle size and performance',
                icon='📦',
                shortcut='b'
            ),
            MenuItem(
                key='metrics',
                label='Performance Metrics',
                description='Track Core Web Vitals',
                icon='📊',
                shortcut='m'
            ),
            MenuItem(
                key='back',
                label='Back to Testing Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'lighthouse':
            run_lighthouse_audit(ui)
        elif choice == 'load':
            run_load_tests(ui)
        elif choice == 'bundle':
            analyze_bundle(ui)
        elif choice == 'metrics':
            track_performance_metrics(ui)

def show_mocking_submenu(ui) -> None:
    """API mocking submenu."""
    while True:
        ui.print_header(
            "API Mocking",
            "Configure and Manage API Mocks"
        )

        menu_items = [
            MenuItem(
                key='create',
                label='Create Mock',
                description='Create new API mock',
                icon='➕',
                shortcut='c'
            ),
            MenuItem(
                key='list',
                label='List Mocks',
                description='View existing mocks',
                icon='📋',
                shortcut='l'
            ),
            MenuItem(
                key='edit',
                label='Edit Mock',
                description='Modify existing mock',
                icon='✏️',
                shortcut='e'
            ),
            MenuItem(
                key='record',
                label='Record API',
                description='Record API responses',
                icon='⏺️',
                shortcut='r'
            ),
            MenuItem(
                key='back',
                label='Back to Testing Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'create':
            create_api_mock(ui)
        elif choice == 'list':
            list_api_mocks(ui)
        elif choice == 'edit':
            edit_api_mock(ui)
        elif choice == 'record':
            record_api_responses(ui)

def show_snapshot_submenu(ui) -> None:
    """Snapshot testing submenu."""
    while True:
        ui.print_header(
            "Snapshot Testing",
            "Manage Component Snapshots"
        )

        menu_items = [
            MenuItem(
                key='run',
                label='Run Snapshots',
                description='Run snapshot tests',
                icon='📸',
                shortcut='r'
            ),
            MenuItem(
                key='update',
                label='Update Snapshots',
                description='Update snapshot files',
                icon='🔄',
                shortcut='u'
            ),
            MenuItem(
                key='inspect',
                label='Inspect Snapshots',
                description='View snapshot contents',
                icon='🔍',
                shortcut='i'
            ),
            MenuItem(
                key='clean',
                label='Clean Snapshots',
                description='Remove obsolete snapshots',
                icon='🧹',
                shortcut='c'
            ),
            MenuItem(
                key='back',
                label='Back to Testing Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'run':
            ui.project.run_npm_command('test:snapshot')
        elif choice == 'update':
            ui.project.run_npm_command('test:snapshot:update')
        elif choice == 'inspect':
            inspect_snapshots(ui)
        elif choice == 'clean':
            clean_snapshots(ui)

def run_lighthouse_audit(ui) -> None:
    """Run Lighthouse performance audit."""
    ui.print_header(
        "Lighthouse Audit",
        "Performance Audit"
    )

    try:
        url = ui.get_input("Enter URL to audit (default: localhost:3000)", required=False) or "http://localhost:3000"
        device = ui.get_input("Device type (mobile/desktop)", required=False) or "desktop"

        if ui.project.run_lighthouse_audit(url, device):
            ui.status_bar.update("Lighthouse audit completed successfully", 3)
        else:
            ui.status_bar.update("Lighthouse audit failed", 3)
    except Exception as e:
        ui.status_bar.update(f"Error running Lighthouse audit: {str(e)}", 3)

def run_load_tests(ui) -> None:
    """Run k6 load tests."""
    ui.print_header(
        "Load Testing",
        "k6 Load Tests"
    )

    tests = ui.project.get_load_tests()
    if not tests:
        ui.status_bar.update("No load tests found", 3)
        return

    print("\nAvailable Load Tests:")
    for i, test in enumerate(tests, 1):
        print(f"{i}. {test}")

    try:
        selection = int(ui.get_input("\nSelect test number", required=True))
        if selection > 0 and selection <= len(tests):
            test = tests[selection-1]
            vus = int(ui.get_input("Number of virtual users", required=True))
            duration = ui.get_input("Test duration (e.g., 30s, 1m)", required=True)

            if ui.project.run_k6_test(test, vus, duration):
                ui.status_bar.update(f"Load test completed successfully", 3)
            else:
                ui.status_bar.update("Load test failed", 3)
        else:
            ui.status_bar.update("Invalid selection", 3)
    except ValueError:
        ui.status_bar.update("Invalid input", 3)

def analyze_bundle(ui) -> None:
    """Analyze bundle size and performance."""
    if ui.project.analyze_bundle():
        ui.status_bar.update("Bundle analysis completed", 3)
    else:
        ui.status_bar.update("Bundle analysis failed", 3)

def track_performance_metrics(ui) -> None:
    """Track Core Web Vitals and performance metrics."""
    if ui.project.track_web_vitals():
        ui.status_bar.update("Performance metrics tracked successfully", 3)
    else:
        ui.status_bar.update("Failed to track performance metrics", 3)

def create_api_mock(ui) -> None:
    """Create new API mock."""
    try:
        endpoint = ui.get_input("API endpoint (e.g., /api/users)", required=True)
        method = ui.get_input("HTTP method (GET/POST/PUT/DELETE)", required=True).upper()
        status = int(ui.get_input("Response status code", required=True))
        response = ui.get_input("Response body (JSON)", required=True)

        if ui.project.create_api_mock(endpoint, method, status, response):
            ui.status_bar.update("API mock created successfully", 3)
        else:
            ui.status_bar.update("Failed to create API mock", 3)
    except ValueError:
        ui.status_bar.update("Invalid input", 3)

def list_api_mocks(ui) -> None:
    """List existing API mocks."""
    mocks = ui.project.get_api_mocks()
    if not mocks:
        ui.status_bar.update("No API mocks found", 3)
        return

    print("\nExisting API Mocks:")
    for mock in mocks:
        print(f"\n{ui.theme.COLORS['HEADER']}{mock['method']} {mock['endpoint']}{ui.theme.COLORS['ENDC']}")
        print(f"Status: {mock['status']}")
        print(f"Response: {mock['response']}")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()

def edit_api_mock(ui) -> None:
    """Edit existing API mock."""
    mocks = ui.project.get_api_mocks()
    if not mocks:
        ui.status_bar.update("No API mocks found", 3)
        return

    print("\nSelect mock to edit:")
    for i, mock in enumerate(mocks, 1):
        print(f"{i}. {mock['method']} {mock['endpoint']}")

    try:
        selection = int(ui.get_input("\nMock number", required=True)) - 1
        if selection < 0 or selection >= len(mocks):
            ui.status_bar.update("Invalid selection", 3)
            return

        mock = mocks[selection]
        print(f"\nEditing mock: {mock['method']} {mock['endpoint']}")
        print("Press Enter to keep current values")

        status = int(ui.get_input(f"Status code [{mock['status']}]") or mock['status'])
        response = ui.get_input(f"Response body [{mock['response']}]") or mock['response']

        if ui.project.update_api_mock(mock['endpoint'], mock['method'], status, response):
            ui.status_bar.update("API mock updated successfully", 3)
        else:
            ui.status_bar.update("Failed to update API mock", 3)
    except ValueError:
        ui.status_bar.update("Invalid input", 3)

def record_api_responses(ui) -> None:
    """Record actual API responses for mocking."""
    try:
        url = ui.get_input("API base URL", required=True)
        duration = ui.get_input("Recording duration (e.g., 5m)", required=True)

        if ui.project.record_api_responses(url, duration):
            ui.status_bar.update("API responses recorded successfully", 3)
        else:
            ui.status_bar.update("Failed to record API responses", 3)
    except Exception as e:
        ui.status_bar.update(f"Error recording API responses: {str(e)}", 3)

def inspect_snapshots(ui) -> None:
    """View snapshot contents."""
    snapshots = ui.project.get_snapshots()
    if not snapshots:
        ui.status_bar.update("No snapshots found", 3)
        return

    print("\nAvailable Snapshots:")
    for i, snapshot in enumerate(snapshots, 1):
        print(f"{i}. {snapshot}")

    try:
        selection = int(ui.get_input("\nSelect snapshot number", required=True)) - 1
        if selection >= 0 and selection < len(snapshots):
            snapshot = snapshots[selection]
            content = ui.project.get_snapshot_content(snapshot)
            print(f"\n{ui.theme.COLORS['HEADER']}Snapshot: {snapshot}{ui.theme.COLORS['ENDC']}")
            print(content)
        else:
            ui.status_bar.update("Invalid selection", 3)
    except ValueError:
        ui.status_bar.update("Invalid input", 3)

def show_integration_submenu(ui) -> None:
    """Integration testing submenu."""
    while True:
        ui.print_header(
            "Integration Tests",
            "Run Integration Test Suites"
        )

        menu_items = [
            MenuItem(
                key='api',
                label='API Tests',
                description='Run API integration tests',
                icon='🌐',
                shortcut='a'
            ),
            MenuItem(
                key='db',
                label='Database Tests',
                description='Run database integration tests',
                icon='💾',
                shortcut='d'
            ),
            MenuItem(
                key='service',
                label='Service Tests',
                description='Run service integration tests',
                icon='⚙️',
                shortcut='s'
            ),
            MenuItem(
                key='all',
                label='Run All',
                description='Run all integration tests',
                icon='▶️',
                shortcut='r'
            ),
            MenuItem(
                key='back',
                label='Back to Testing Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'api':
            ui.project.test_manager.run_integration_tests('api')
        elif choice == 'db':
            ui.project.test_manager.run_integration_tests('database')
        elif choice == 'service':
            ui.project.test_manager.run_integration_tests('service')
        elif choice == 'all':
            ui.project.test_manager.run_integration_tests('all')

def show_test_data_submenu(ui) -> None:
    """Test data management submenu."""
    while True:
        ui.print_header(
            "Test Data Management",
            "Manage Test Data and Fixtures"
        )

        menu_items = [
            MenuItem(
                key='fixture',
                label='Generate Fixture',
                description='Create new test fixture',
                icon='📝',
                shortcut='f'
            ),
            MenuItem(
                key='mock',
                label='Create Mock',
                description='Create mock test data',
                icon='🔄',
                shortcut='m'
            ),
            MenuItem(
                key='seed',
                label='Seed Database',
                description='Seed test database with fixtures',
                icon='🌱',
                shortcut='s'
            ),
            MenuItem(
                key='back',
                label='Back to Testing Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'fixture':
            create_test_fixture(ui)
        elif choice == 'mock':
            create_mock_data(ui)
        elif choice == 'seed':
            seed_test_database(ui)

def show_reporting_submenu(ui) -> None:
    """Test reporting submenu."""
    while True:
        ui.print_header(
            "Test Reports",
            "View and Analyze Test Results"
        )

        menu_items = [
            MenuItem(
                key='generate',
                label='Generate Report',
                description='Generate test report',
                icon='📊',
                shortcut='g'
            ),
            MenuItem(
                key='history',
                label='View History',
                description='View test run history',
                icon='📋',
                shortcut='h'
            ),
            MenuItem(
                key='trends',
                label='Analyze Trends',
                description='View test trends and patterns',
                icon='📈',
                shortcut='t'
            ),
            MenuItem(
                key='back',
                label='Back to Testing Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'generate':
            generate_test_report(ui)
        elif choice == 'history':
            view_test_history(ui)
        elif choice == 'trends':
            analyze_test_trends(ui)

def create_test_fixture(ui) -> None:
    """Create a new test fixture."""
    try:
        name = ui.get_input("Fixture name", required=True)
        print("\nEnter fixture schema (JSON format):")
        schema_str = ui.get_input("Schema", required=True)
        schema = json.loads(schema_str)

        if ui.project.test_manager.generate_test_fixture(name, schema):
            ui.status_bar.update("Test fixture created successfully", 3)
        else:
            ui.status_bar.update("Failed to create test fixture", 3)
    except json.JSONDecodeError:
        ui.status_bar.update("Invalid JSON schema", 3)
    except Exception as e:
        ui.status_bar.update(f"Error: {str(e)}", 3)

def create_mock_data(ui) -> None:
    """Create mock test data."""
    try:
        name = ui.get_input("Mock data name", required=True)
        print("\nEnter mock data (JSON format):")
        data_str = ui.get_input("Data", required=True)
        data = json.loads(data_str)

        if ui.project.test_manager.create_mock_data(name, data):
            ui.status_bar.update("Mock data created successfully", 3)
        else:
            ui.status_bar.update("Failed to create mock data", 3)
    except json.JSONDecodeError:
        ui.status_bar.update("Invalid JSON data", 3)
    except Exception as e:
        ui.status_bar.update(f"Error: {str(e)}", 3)

def seed_test_database(ui) -> None:
    """Seed test database with fixture data."""
    try:
        fixture = ui.get_input("Fixture name (optional)", required=False)
        if ui.project.test_manager.seed_test_database(fixture):
            ui.status_bar.update("Database seeded successfully", 3)
        else:
            ui.status_bar.update("Failed to seed database", 3)
    except Exception as e:
        ui.status_bar.update(f"Error: {str(e)}", 3)

def generate_test_report(ui) -> None:
    """Generate a test report."""
    try:
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        if ui.project.test_manager.generate_test_report(run_id):
            ui.status_bar.update("Test report generated successfully", 3)
        else:
            ui.status_bar.update("Failed to generate test report", 3)
    except Exception as e:
        ui.status_bar.update(f"Error: {str(e)}", 3)

def view_test_history(ui) -> None:
    """View test run history."""
    history = ui.project.test_manager.track_test_history()
    if not history:
        ui.status_bar.update("No test history found", 3)
        return

    print("\nTest Run History:")
    for report in history:
        summary = report['summary']
        print(f"\n{ui.theme.COLORS['HEADER']}Run ID: {report['run_id']}{ui.theme.COLORS['ENDC']}")
        print(f"Timestamp: {report['timestamp']}")
        print(f"Total Tests: {summary['total']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Duration: {summary['duration']}s")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()

def analyze_test_trends(ui) -> None:
    """Analyze test trends and patterns."""
    trends = ui.project.test_manager.analyze_test_trends()
    if not trends:
        ui.status_bar.update("No trend data available", 3)
        return

    print("\nTest Trends Analysis:")

    # Pass rate trend
    if trends['pass_rate']:
        avg_pass_rate = sum(trends['pass_rate']) / len(trends['pass_rate'])
        print(f"\n{ui.theme.COLORS['HEADER']}Pass Rate{ui.theme.COLORS['ENDC']}")
        print(f"Average: {avg_pass_rate:.2f}%")
        print(f"Latest: {trends['pass_rate'][0]:.2f}%")

    # Duration trend
    if trends['duration']:
        avg_duration = sum(trends['duration']) / len(trends['duration'])
        print(f"\n{ui.theme.COLORS['HEADER']}Test Duration{ui.theme.COLORS['ENDC']}")
        print(f"Average: {avg_duration:.2f}s")
        print(f"Latest: {trends['duration'][0]:.2f}s")

    # Failure patterns
    if trends['failure_patterns']:
        print(f"\n{ui.theme.COLORS['HEADER']}Common Failures{ui.theme.COLORS['ENDC']}")
        for test, count in sorted(trends['failure_patterns'].items(), key=lambda x: x[1], reverse=True):
            print(f"{test}: {count} failures")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()

def clean_snapshots(ui) -> None:
    """Remove obsolete snapshots."""
    if ui.project.clean_snapshots():
        ui.status_bar.update("Obsolete snapshots removed successfully", 3)
    else:
        ui.status_bar.update("Failed to clean snapshots", 3)
