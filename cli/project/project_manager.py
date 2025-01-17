"""Project management functionality."""

from typing import Dict, Any, List, Optional
from .debug_manager import DebugManager
from .code_quality_manager import CodeQualityManager
from .typescript_manager import TypeScriptManager
from .npm_manager import NPMManager
from .git_manager import GitManager
from .test_manager import TestManager
from .config_manager import ConfigManager
from .compound_manager import CompoundManager, CompoundData
from .performance_manager import PerformanceManager
from .bundle_manager import BundleManager
from .environment_manager import EnvironmentManager
from .dependency_manager import DependencyManager
from .documentation_manager import DocumentationManager
from .scaffold_manager import ScaffoldManager
from .logging_manager import LoggingManager

class ProjectManager:
    """Handles project-specific operations."""
    def __init__(self, ui):
        self.ui = ui
        self.project_root = "/Users/drunkonjava/Desktop/HelloWorldGitHub"

        # Initialize specialized managers
        self.debug_manager = DebugManager(ui)
        self.code_quality_manager = CodeQualityManager(ui)
        self.typescript_manager = TypeScriptManager(ui)
        self.npm_manager = NPMManager(ui)
        self.git_manager = GitManager(ui)
        self.test_manager = TestManager(ui)
        self.config_manager = ConfigManager(ui)
        self.compound_manager = CompoundManager(ui, self.npm_manager)
        self.performance_manager = PerformanceManager(ui)
        self.bundle_manager = BundleManager(ui)
        self.environment_manager = EnvironmentManager(ui)
        self.dependency_manager = DependencyManager(self.project_root)
        self.documentation_manager = DocumentationManager(self.project_root)
        self.scaffold_manager = ScaffoldManager(self.project_root)
        self.logging_manager = LoggingManager(self.project_root)

    # NPM and Project Operations
    def run_npm_command(self, command: str) -> bool:
        """Run an npm command."""
        return self.npm_manager.run_npm_command(command)

    def clean_build(self) -> bool:
        """Clean build artifacts and node_modules."""
        return self.npm_manager.clean_build()

    def get_project_status(self) -> Dict[str, Any]:
        """Get current project status and information."""
        return self.npm_manager.get_project_status()

    # Git Operations
    def get_repo_status(self) -> Dict[str, Any]:
        """Get repository status information."""
        return self.git_manager.get_repo_status()

    def manage_branches(self, action: str, branch_name: str = '') -> bool:
        """Manage Git branches."""
        return self.git_manager.manage_branches(action, branch_name)

    def sync_repository(self) -> bool:
        """Sync with remote repository."""
        return self.git_manager.sync_repository()

    def manage_issues(self, action: str, issue_data: Dict = None) -> bool:
        """Manage GitHub issues."""
        return self.git_manager.manage_issues(action, issue_data)

    def manage_secrets(self, action: str, secret_data: Dict = None) -> bool:
        """Manage GitHub secrets."""
        return self.git_manager.manage_secrets(action, secret_data)

    def configure_pages_settings(self) -> bool:
        """Configure GitHub Pages settings."""
        return self.git_manager.configure_pages_settings()

    # Testing Operations
    def get_testable_components(self) -> List[str]:
        """Get list of components with test files."""
        return self.test_manager.get_testable_components()

    def run_component_tests(self, component_path: str) -> bool:
        """Run tests for a specific component."""
        return self.test_manager.run_component_tests(component_path)

    def debug_e2e_test(self, test_name: str = '') -> bool:
        """Run E2E tests in debug mode."""
        return self.test_manager.debug_e2e_test(test_name)

    def generate_coverage_badge(self) -> bool:
        """Generate coverage badge from coverage report."""
        return self.test_manager.generate_coverage_badge()

    def run_test_suite(self, test_type: str = 'all') -> bool:
        """Run the test suite with specified type."""
        return self.test_manager.run_test_suite(test_type)

    def watch_tests(self, component_path: str = '') -> bool:
        """Run tests in watch mode."""
        return self.test_manager.watch_tests(component_path)

    # Configuration Operations
    def configure_host(self, host: str, port: int) -> bool:
        """Configure development server host and port."""
        return self.config_manager.configure_host(host, port)

    def get_host_config(self) -> Dict[str, Any]:
        """Get current host configuration."""
        return self.config_manager.get_host_config()

    def update_package_json(self, updates: Dict[str, Any]) -> bool:
        """Update package.json with provided updates."""
        return self.config_manager.update_package_json(updates)

    def get_config(self, config_name: str) -> Dict[str, Any]:
        """Get configuration by name."""
        return self.config_manager.get_config(config_name)

    # Compound Operations
    def get_compounds(self) -> List[Dict[str, Any]]:
        """Get list of all compounds."""
        return self.compound_manager.get_compounds()

    def add_compound(self, compound_data: CompoundData) -> bool:
        """Add a new compound."""
        return self.compound_manager.add_compound(compound_data)

    def edit_compound(self, compound_name: str, updated_data: CompoundData) -> bool:
        """Edit an existing compound."""
        return self.compound_manager.edit_compound(compound_name, updated_data)

    def validate_compound_data(self, compound: Dict[str, Any]) -> List[str]:
        """Validate compound data structure."""
        return self.compound_manager.validate_compound_data(compound)

    def generate_compound_page(self, compound_name: str) -> bool:
        """Generate or update compound page."""
        return self.compound_manager.generate_compound_page(compound_name)

    def get_compound_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get compound data by name."""
        return self.compound_manager.get_compound_by_name(name)

    def get_compound_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get compound data by slug."""
        return self.compound_manager.get_compound_by_slug(slug)

    # Performance Management
    def run_cpu_profiling(self, duration: int) -> bool:
        """Run CPU profiling."""
        return self.performance_manager.run_cpu_profiling(duration)

    def run_memory_analysis(self) -> bool:
        """Run memory usage analysis."""
        return self.performance_manager.run_memory_analysis()

    def run_network_analysis(self, duration: int) -> bool:
        """Run network request profiling."""
        return self.performance_manager.run_network_analysis(duration)

    def generate_flame_graph(self, duration: int) -> bool:
        """Generate CPU flame graph."""
        return self.performance_manager.generate_flame_graph(duration)

    def track_web_vitals(self) -> bool:
        """Track Core Web Vitals metrics."""
        return self.performance_manager.track_web_vitals()

    # Bundle Management
    def analyze_bundle_size(self) -> bool:
        """Analyze bundle size and composition."""
        return self.bundle_manager.analyze_bundle_size()

    def analyze_dependencies(self) -> bool:
        """Analyze project dependencies."""
        return self.bundle_manager.analyze_dependencies()

    def find_unused_code(self) -> bool:
        """Find unused code and imports."""
        return self.bundle_manager.find_unused_code()

    def optimize_bundle(self) -> bool:
        """Optimize bundle size."""
        return self.bundle_manager.optimize_bundle()

    def get_bundle_stats(self) -> Optional[Dict[str, Any]]:
        """Get bundle statistics."""
        return self.bundle_manager.get_bundle_stats()

    # Debug Operations
    def configure_debugger(self, config: Dict[str, Any]) -> bool:
        """Configure debugger settings."""
        return self.debug_manager.configure_debugger(config)

    def manage_breakpoints(self, action: str, data: Dict[str, Any] = None) -> bool:
        """Manage breakpoints."""
        return self.debug_manager.manage_breakpoints(action, data)

    def inspect_variable(self, variable_name: str) -> Optional[Dict[str, Any]]:
        """Inspect variable during debugging."""
        return self.debug_manager.inspect_variable(variable_name)

    def get_call_stack(self) -> List[Dict[str, Any]]:
        """Get current call stack."""
        return self.debug_manager.get_call_stack()

    def get_debug_console(self) -> List[str]:
        """Get debug console output."""
        return self.debug_manager.get_debug_console()

    def start_debug_session(self, config_name: str = '') -> bool:
        """Start a debug session."""
        return self.debug_manager.start_debug_session(config_name)

    def stop_debug_session(self) -> bool:
        """Stop the current debug session."""
        return self.debug_manager.stop_debug_session()

    # Environment Management
    def get_environment_variables(self) -> Dict[str, str]:
        """Get current environment variables."""
        return self.environment_manager.get_environment_variables()

    def add_environment_variable(self, key: str, value: str) -> bool:
        """Add new environment variable."""
        return self.environment_manager.add_environment_variable(key, value)

    def update_environment_variable(self, key: str, value: str) -> bool:
        """Update existing environment variable."""
        return self.environment_manager.update_environment_variable(key, value)

    def delete_environment_variable(self, key: str) -> bool:
        """Delete environment variable."""
        return self.environment_manager.delete_environment_variable(key)

    def validate_environment_config(self) -> List[str]:
        """Validate environment configuration."""
        return self.environment_manager.validate_environment_config()

    # Code Quality Operations
    def configure_eslint(self, config: Dict[str, Any]) -> bool:
        """Configure ESLint settings."""
        return self.code_quality_manager.configure_eslint(config)

    def configure_prettier(self, config: Dict[str, Any]) -> bool:
        """Configure Prettier settings."""
        return self.code_quality_manager.configure_prettier(config)

    def run_eslint(self, fix: bool = False) -> List[Dict[str, Any]]:
        """Run ESLint on project files."""
        return self.code_quality_manager.run_eslint(fix)

    def run_prettier(self, write: bool = False) -> List[str]:
        """Run Prettier on project files."""
        return self.code_quality_manager.run_prettier(write)

    def get_style_guide_violations(self) -> List[Dict[str, Any]]:
        """Get style guide violations."""
        return self.code_quality_manager.get_style_guide_violations()

    def enforce_style_guide(self) -> bool:
        """Enforce style guide rules."""
        return self.code_quality_manager.enforce_style_guide()

    def get_code_quality_report(self) -> Dict[str, Any]:
        """Generate code quality report."""
        return self.code_quality_manager.get_code_quality_report()

    def format_file(self, file_path: str) -> bool:
        """Format a specific file."""
        return self.code_quality_manager.format_file(file_path)

    def format_directory(self, directory: str) -> bool:
        """Format all files in a directory."""
        return self.code_quality_manager.format_directory(directory)

    def get_formatting_config(self) -> Dict[str, Any]:
        """Get current formatting configuration."""
        return self.code_quality_manager.get_formatting_config()

    def update_formatting_config(self, config: Dict[str, Any]) -> bool:
        """Update formatting configuration."""
        return self.code_quality_manager.update_formatting_config(config)

    # TypeScript Operations
    def check_types(self, path: str = '') -> List[Dict[str, Any]]:
        """Run TypeScript type checking."""
        return self.typescript_manager.check_types(path)

    def generate_types(self, source_path: str) -> bool:
        """Generate TypeScript types from JavaScript files."""
        return self.typescript_manager.generate_types(source_path)

    def manage_declarations(self, action: str, data: Dict[str, Any] = None) -> bool:
        """Manage declaration files."""
        return self.typescript_manager.manage_declarations(action, data)

    def get_type_coverage(self) -> Dict[str, Any]:
        """Get type coverage report."""
        return self.typescript_manager.get_type_coverage()

    def validate_types(self, strict: bool = False) -> List[str]:
        """Validate TypeScript types with optional strict mode."""
        return self.typescript_manager.validate_types(strict)

    def update_tsconfig(self, config: Dict[str, Any]) -> bool:
        """Update TypeScript configuration."""
        return self.typescript_manager.update_tsconfig(config)

    def get_tsconfig(self) -> Dict[str, Any]:
        """Get current TypeScript configuration."""
        return self.typescript_manager.get_tsconfig()

    def organize_imports(self, file_path: str = '') -> bool:
        """Organize TypeScript imports."""
        return self.typescript_manager.organize_imports(file_path)

    def find_type_errors(self, path: str = '') -> List[Dict[str, Any]]:
        """Find TypeScript type errors."""
        return self.typescript_manager.find_type_errors(path)

    def suggest_types(self, file_path: str) -> List[Dict[str, Any]]:
        """Suggest types for untyped code."""
        return self.typescript_manager.suggest_types(file_path)

    # Scaffolding Operations
    def get_available_templates(self) -> List[str]:
        """Get list of available project templates."""
        return self.scaffold_manager.get_available_templates()

    def validate_template(self, template_name: str) -> List[str]:
        """Validate template structure and configuration."""
        return self.scaffold_manager.validate_template(template_name)

    def create_project(self, template_name: str, project_name: str,
                      config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new project from template."""
        return self.scaffold_manager.create_project(template_name, project_name, config)

    def create_component(self, component_name: str,
                        template: str = 'default') -> Dict[str, Any]:
        """Create a new component from template."""
        return self.scaffold_manager.create_component(component_name, template)

    def create_page(self, page_name: str,
                   template: str = 'default') -> Dict[str, Any]:
        """Create a new page from template."""
        return self.scaffold_manager.create_page(page_name, template)

    def create_test(self, target_path: str,
                   template: str = 'default') -> Dict[str, Any]:
        """Create a test file for a component or page."""
        return self.scaffold_manager.create_test(target_path, template)
