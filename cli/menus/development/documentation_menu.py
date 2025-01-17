"""Documentation menu implementation."""

from ...models.menu_item import MenuItem

def show_documentation_submenu(ui) -> None:
    """Documentation tools submenu."""
    while True:
        ui.print_header(
            "Documentation Tools",
            "Generate and Manage Documentation"
        )

        menu_items = [
            MenuItem(
                key='api',
                label='Generate API Docs',
                description='Generate API documentation',
                icon='📚',
                shortcut='a'
            ),
            MenuItem(
                key='component',
                label='Component Docs',
                description='Generate component documentation',
                icon='🧩',
                shortcut='c'
            ),
            MenuItem(
                key='markdown',
                label='Markdown Files',
                description='Manage markdown documentation',
                icon='📝',
                shortcut='m'
            ),
            MenuItem(
                key='list',
                label='List Files',
                description='List documentation files',
                icon='📋',
                shortcut='l'
            ),
            MenuItem(
                key='index',
                label='Generate Index',
                description='Generate documentation index',
                icon='📑',
                shortcut='i'
            ),
            MenuItem(
                key='validate',
                label='Validate Docs',
                description='Validate documentation files',
                icon='✓',
                shortcut='v'
            ),
            MenuItem(
                key='backup',
                label='Backup Docs',
                description='Create documentation backup',
                icon='💾',
                shortcut='b'
            ),
            MenuItem(
                key='back',
                label='Back to Development Menu',
                icon='◀',
                shortcut='k'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'api':
            if ui.project.documentation_manager.generate_api_docs():
                ui.status_bar.update("API documentation generated successfully", 3)
            else:
                ui.status_bar.update("Failed to generate API documentation", 3)
        elif choice == 'component':
            if ui.project.documentation_manager.generate_component_docs():
                ui.status_bar.update("Component documentation generated successfully", 3)
            else:
                ui.status_bar.update("Failed to generate component documentation", 3)
        elif choice == 'markdown':
            manage_markdown_documentation(ui)
        elif choice == 'list':
            files = ui.project.documentation_manager.list_documentation_files()
            if files:
                print("\nDocumentation Files:")
                for file in files:
                    print(f"- {file['path']} ({file['type']}, {file['size']} bytes)")
                print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
                input()
            else:
                ui.status_bar.update("No documentation files found", 3)
        elif choice == 'index':
            if ui.project.documentation_manager.generate_documentation_index():
                ui.status_bar.update("Documentation index generated successfully", 3)
            else:
                ui.status_bar.update("Failed to generate documentation index", 3)
        elif choice == 'validate':
            issues = ui.project.documentation_manager.validate_documentation()
            if issues:
                print("\nDocumentation Issues:")
                for issue in issues:
                    print(f"- {issue['file']} (line {issue['line']}): {issue['issue']}")
                print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
                input()
            else:
                ui.status_bar.update("No documentation issues found", 3)
        elif choice == 'backup':
            if ui.project.documentation_manager.backup_documentation():
                ui.status_bar.update("Documentation backup created successfully", 3)
            else:
                ui.status_bar.update("Failed to create documentation backup", 3)

def manage_markdown_documentation(ui) -> None:
    """Manage markdown documentation files."""
    while True:
        ui.print_header(
            "Markdown Documentation",
            "Manage Markdown Files"
        )

        menu_items = [
            MenuItem(
                key='create',
                label='Create File',
                description='Create new markdown file',
                icon='➕',
                shortcut='c'
            ),
            MenuItem(
                key='update',
                label='Update File',
                description='Update existing markdown file',
                icon='✏️',
                shortcut='u'
            ),
            MenuItem(
                key='delete',
                label='Delete File',
                description='Delete markdown file',
                icon='🗑️',
                shortcut='d'
            ),
            MenuItem(
                key='back',
                label='Back to Documentation Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'create':
            file_path = ui.get_input("File path (relative to docs)", required=True)
            content = ui.get_input("File content", required=True)
            if ui.project.documentation_manager.manage_markdown_files('create', file_path, content):
                ui.status_bar.update("Markdown file created successfully", 3)
            else:
                ui.status_bar.update("Failed to create markdown file", 3)
        elif choice == 'update':
            file_path = ui.get_input("File path (relative to docs)", required=True)
            content = ui.get_input("New content", required=True)
            if ui.project.documentation_manager.manage_markdown_files('update', file_path, content):
                ui.status_bar.update("Markdown file updated successfully", 3)
            else:
                ui.status_bar.update("Failed to update markdown file", 3)
        elif choice == 'delete':
            file_path = ui.get_input("File path (relative to docs)", required=True)
            confirm = ui.get_input(f"Are you sure you want to delete {file_path}? (y/n)").lower()
            if confirm == 'y':
                if ui.project.documentation_manager.manage_markdown_files('delete', file_path):
                    ui.status_bar.update("Markdown file deleted successfully", 3)
                else:
                    ui.status_bar.update("Failed to delete markdown file", 3)

def show_dependency_submenu(ui) -> None:
    """Dependency management submenu."""
    while True:
        ui.print_header(
            "Dependency Management",
            "Manage Project Dependencies"
        )

        menu_items = [
            MenuItem(
                key='check',
                label='Check Updates',
                description='Check for dependency updates',
                icon='🔄',
                shortcut='c'
            ),
            MenuItem(
                key='scan',
                label='Security Scan',
                description='Scan for vulnerabilities',
                icon='🔒',
                shortcut='s'
            ),
            MenuItem(
                key='update',
                label='Update Package',
                description='Update specific package',
                icon='⬆️',
                shortcut='u'
            ),
            MenuItem(
                key='list',
                label='List Versions',
                description='List installed versions',
                icon='📋',
                shortcut='l'
            ),
            MenuItem(
                key='fix',
                label='Fix Vulnerabilities',
                description='Fix security vulnerabilities',
                icon='🔧',
                shortcut='f'
            ),
            MenuItem(
                key='tree',
                label='Dependency Tree',
                description='View dependency tree',
                icon='🌳',
                shortcut='t'
            ),
            MenuItem(
                key='back',
                label='Back to Development Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'check':
            updates = ui.project.dependency_manager.check_updates()
            if updates:
                print("\nAvailable Updates:")
                for pkg, version in updates.items():
                    print(f"- {pkg}: {version}")
                print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
                input()
            else:
                ui.status_bar.update("All dependencies are up to date", 3)
        elif choice == 'scan':
            vulnerabilities = ui.project.dependency_manager.scan_vulnerabilities()
            if vulnerabilities:
                print("\nVulnerabilities Found:")
                for vuln in vulnerabilities:
                    print(f"- {vuln.get('package')}: {vuln.get('severity')} - {vuln.get('title')}")
                print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
                input()
            else:
                ui.status_bar.update("No vulnerabilities found", 3)
        elif choice == 'update':
            package = ui.get_input("Package name", required=True)
            version = ui.get_input("Version (optional)")
            if ui.project.dependency_manager.update_package(package, version):
                ui.status_bar.update(f"Updated {package} successfully", 3)
            else:
                ui.status_bar.update(f"Failed to update {package}", 3)
        elif choice == 'list':
            versions = ui.project.dependency_manager.get_installed_versions()
            if versions:
                print("\nInstalled Versions:")
                for pkg, version in versions.items():
                    print(f"- {pkg}: {version}")
                print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
                input()
            else:
                ui.status_bar.update("No dependencies found", 3)
        elif choice == 'fix':
            if ui.project.dependency_manager.fix_vulnerabilities():
                ui.status_bar.update("Vulnerabilities fixed successfully", 3)
            else:
                ui.status_bar.update("Failed to fix vulnerabilities", 3)
        elif choice == 'tree':
            tree = ui.project.dependency_manager.get_dependency_tree()
            if tree:
                print("\nDependency Tree:")
                print(json.dumps(tree, indent=2))
                print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
                input()
            else:
                ui.status_bar.update("Failed to get dependency tree", 3)
