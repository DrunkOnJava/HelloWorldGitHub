"""Project scaffolding functionality."""

from typing import Dict, Any, List, Optional
import os
import json
import shutil
from pathlib import Path

class ScaffoldManager:
    """Handles project scaffolding operations."""

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.templates_dir = os.path.join(project_root, 'src', 'templates')

    def get_available_templates(self) -> List[str]:
        """Get list of available project templates."""
        if not os.path.exists(self.templates_dir):
            return []
        return [d for d in os.listdir(self.templates_dir)
                if os.path.isdir(os.path.join(self.templates_dir, d))]

    def validate_template(self, template_name: str) -> List[str]:
        """Validate template structure and configuration."""
        errors = []
        template_path = os.path.join(self.templates_dir, template_name)

        if not os.path.exists(template_path):
            errors.append(f"Template '{template_name}' does not exist")
            return errors

        # Check for required template files
        required_files = ['template.json', 'structure.json']
        for file in required_files:
            if not os.path.exists(os.path.join(template_path, file)):
                errors.append(f"Missing required file: {file}")

        return errors

    def create_project(self, template_name: str, project_name: str,
                      config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a new project from template."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'created_files': []
        }

        # Validate template
        errors = self.validate_template(template_name)
        if errors:
            result['errors'].extend(errors)
            return result

        template_path = os.path.join(self.templates_dir, template_name)
        project_path = os.path.join(self.project_root, project_name)

        try:
            # Load template configuration
            with open(os.path.join(template_path, 'template.json')) as f:
                template_config = json.load(f)

            # Load structure definition
            with open(os.path.join(template_path, 'structure.json')) as f:
                structure = json.load(f)

            # Create project directory
            os.makedirs(project_path, exist_ok=True)

            # Generate project structure
            self._generate_structure(structure, template_path, project_path,
                                  project_name, config or {}, result)

            # Copy template files
            self._copy_template_files(template_path, project_path,
                                   template_config.get('files', []), result)

            # Process dependencies
            if 'dependencies' in template_config:
                self._process_dependencies(project_path,
                                        template_config['dependencies'],
                                        result)

            result['success'] = True

        except Exception as e:
            result['errors'].append(f"Project creation failed: {str(e)}")
            # Cleanup on failure
            if os.path.exists(project_path):
                shutil.rmtree(project_path)

        return result

    def _generate_structure(self, structure: Dict[str, Any], template_path: str,
                          project_path: str, project_name: str,
                          config: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Generate project directory structure."""
        for dir_name, contents in structure.items():
            dir_path = os.path.join(project_path, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            result['created_files'].append(dir_path)

            if isinstance(contents, dict):
                self._generate_structure(contents, template_path, dir_path,
                                      project_name, config, result)

    def _copy_template_files(self, template_path: str, project_path: str,
                           files: List[str], result: Dict[str, Any]) -> None:
        """Copy template files to project directory."""
        for file in files:
            src = os.path.join(template_path, file)
            dst = os.path.join(project_path, file)

            if os.path.exists(src):
                shutil.copy2(src, dst)
                result['created_files'].append(dst)
            else:
                result['warnings'].append(f"Template file not found: {file}")

    def _process_dependencies(self, project_path: str,
                            dependencies: Dict[str, str],
                            result: Dict[str, Any]) -> None:
        """Process project dependencies."""
        package_json_path = os.path.join(project_path, 'package.json')

        try:
            if os.path.exists(package_json_path):
                with open(package_json_path) as f:
                    package_data = json.load(f)
            else:
                package_data = {
                    'name': os.path.basename(project_path),
                    'version': '1.0.0',
                    'dependencies': {},
                    'devDependencies': {}
                }

            # Update dependencies
            package_data['dependencies'].update(dependencies.get('prod', {}))
            package_data['devDependencies'].update(dependencies.get('dev', {}))

            # Write updated package.json
            with open(package_json_path, 'w') as f:
                json.dump(package_data, f, indent=2)

            result['created_files'].append(package_json_path)

        except Exception as e:
            result['warnings'].append(f"Failed to process dependencies: {str(e)}")

    def create_component(self, component_name: str,
                        template: str = 'default') -> Dict[str, Any]:
        """Create a new component from template."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'created_files': []
        }

        template_path = os.path.join(self.templates_dir, 'components', template)
        if not os.path.exists(template_path):
            result['errors'].append(f"Component template '{template}' not found")
            return result

        try:
            component_path = os.path.join(self.project_root, 'src', 'components',
                                        component_name)
            os.makedirs(component_path, exist_ok=True)

            # Copy component template files
            for file in os.listdir(template_path):
                if file.endswith(('.tsx', '.ts', '.css')):
                    src = os.path.join(template_path, file)
                    dst = os.path.join(component_path,
                                     file.replace('Component', component_name))
                    shutil.copy2(src, dst)
                    result['created_files'].append(dst)

            result['success'] = True

        except Exception as e:
            result['errors'].append(f"Component creation failed: {str(e)}")

        return result

    def create_page(self, page_name: str,
                   template: str = 'default') -> Dict[str, Any]:
        """Create a new page from template."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'created_files': []
        }

        template_path = os.path.join(self.templates_dir, 'pages', template)
        if not os.path.exists(template_path):
            result['errors'].append(f"Page template '{template}' not found")
            return result

        try:
            page_path = os.path.join(self.project_root, 'src', 'pages',
                                   page_name)
            os.makedirs(page_path, exist_ok=True)

            # Copy page template files
            for file in os.listdir(template_path):
                if file.endswith(('.tsx', '.ts', '.css')):
                    src = os.path.join(template_path, file)
                    dst = os.path.join(page_path,
                                     file.replace('Page', page_name))
                    shutil.copy2(src, dst)
                    result['created_files'].append(dst)

            result['success'] = True

        except Exception as e:
            result['errors'].append(f"Page creation failed: {str(e)}")

        return result

    def create_test(self, target_path: str,
                   template: str = 'default') -> Dict[str, Any]:
        """Create a test file for a component or page."""
        result = {
            'success': False,
            'errors': [],
            'warnings': [],
            'created_files': []
        }

        template_path = os.path.join(self.templates_dir, 'tests', template)
        if not os.path.exists(template_path):
            result['errors'].append(f"Test template '{template}' not found")
            return result

        try:
            # Determine test file path
            target_name = os.path.basename(target_path)
            test_dir = os.path.join(os.path.dirname(target_path), '__tests__')
            os.makedirs(test_dir, exist_ok=True)

            # Copy test template
            test_file = f"{target_name}.test.tsx"
            src = os.path.join(template_path, 'Component.test.tsx')
            dst = os.path.join(test_dir, test_file)

            if os.path.exists(src):
                shutil.copy2(src, dst)
                result['created_files'].append(dst)
                result['success'] = True
            else:
                result['errors'].append("Test template file not found")

        except Exception as e:
            result['errors'].append(f"Test creation failed: {str(e)}")

        return result
