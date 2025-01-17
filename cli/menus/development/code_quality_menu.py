"""Code quality menu implementation."""

from ...models.menu_item import MenuItem

def show_code_quality_submenu(ui) -> None:
    """Code quality tools submenu."""
    while True:
        ui.print_header(
            "Code Quality",
            "Code Formatting and Style"
        )

        menu_items = [
            MenuItem(
                key='eslint',
                label='ESLint',
                description='Configure and run ESLint',
                icon='🔍',
                shortcut='e'
            ),
            MenuItem(
                key='prettier',
                label='Prettier',
                description='Configure and run Prettier',
                icon='🎨',
                shortcut='p'
            ),
            MenuItem(
                key='style',
                label='Style Guide',
                description='Manage style guide rules',
                icon='📋',
                shortcut='s'
            ),
            MenuItem(
                key='format',
                label='Format Code',
                description='Format files and directories',
                icon='✨',
                shortcut='f'
            ),
            MenuItem(
                key='report',
                label='Quality Report',
                description='Generate code quality report',
                icon='📊',
                shortcut='r'
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
        elif choice == 'eslint':
            manage_eslint(ui)
        elif choice == 'prettier':
            manage_prettier(ui)
        elif choice == 'style':
            manage_style_guide(ui)
        elif choice == 'format':
            format_code(ui)
        elif choice == 'report':
            generate_quality_report(ui)

def manage_eslint(ui) -> None:
    """Manage ESLint configuration and execution."""
    while True:
        ui.print_header(
            "ESLint Management",
            "Configure and Run ESLint"
        )

        menu_items = [
            MenuItem(
                key='config',
                label='Configure ESLint',
                description='Update ESLint configuration',
                icon='⚙️',
                shortcut='c'
            ),
            MenuItem(
                key='run',
                label='Run ESLint',
                description='Check code with ESLint',
                icon='▶️',
                shortcut='r'
            ),
            MenuItem(
                key='fix',
                label='Fix Issues',
                description='Auto-fix ESLint issues',
                icon='🔧',
                shortcut='f'
            ),
            MenuItem(
                key='back',
                label='Back to Code Quality Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'config':
            config = {
                'rules': ui.get_input("ESLint rules (comma-separated)", required=True),
                'plugins': ui.get_input("ESLint plugins (comma-separated)"),
                'extends': ui.get_input("ESLint extends (comma-separated)")
            }
            if ui.project.configure_eslint(config):
                ui.status_bar.update("ESLint configured successfully", 3)
            else:
                ui.status_bar.update("Failed to configure ESLint", 3)
        elif choice == 'run':
            issues = ui.project.run_eslint(fix=False)
            if issues:
                print("\nESLint Issues:")
                for issue in issues:
                    print(f"- {issue.get('message', 'Unknown issue')}")
                print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
                input()
            else:
                ui.status_bar.update("No ESLint issues found", 3)
        elif choice == 'fix':
            if ui.project.run_eslint(fix=True):
                ui.status_bar.update("ESLint fixes applied successfully", 3)
            else:
                ui.status_bar.update("Failed to apply ESLint fixes", 3)

def manage_prettier(ui) -> None:
    """Manage Prettier configuration and execution."""
    while True:
        ui.print_header(
            "Prettier Management",
            "Configure and Run Prettier"
        )

        menu_items = [
            MenuItem(
                key='config',
                label='Configure Prettier',
                description='Update Prettier configuration',
                icon='⚙️',
                shortcut='c'
            ),
            MenuItem(
                key='check',
                label='Check Formatting',
                description='Check code formatting',
                icon='👁️',
                shortcut='k'
            ),
            MenuItem(
                key='format',
                label='Format Code',
                description='Apply Prettier formatting',
                icon='✨',
                shortcut='f'
            ),
            MenuItem(
                key='back',
                label='Back to Code Quality Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'config':
            config = {
                'tabWidth': int(ui.get_input("Tab width", required=True)),
                'useTabs': ui.get_input("Use tabs? (y/n)", required=True).lower() == 'y',
                'semi': ui.get_input("Use semicolons? (y/n)", required=True).lower() == 'y',
                'singleQuote': ui.get_input("Use single quotes? (y/n)", required=True).lower() == 'y'
            }
            if ui.project.configure_prettier(config):
                ui.status_bar.update("Prettier configured successfully", 3)
            else:
                ui.status_bar.update("Failed to configure Prettier", 3)
        elif choice == 'check':
            files = ui.project.run_prettier(write=False)
            if files:
                print("\nFiles needing formatting:")
                for file in files:
                    print(f"- {file}")
                print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
                input()
            else:
                ui.status_bar.update("All files are properly formatted", 3)
        elif choice == 'format':
            if ui.project.run_prettier(write=True):
                ui.status_bar.update("Code formatted successfully", 3)
            else:
                ui.status_bar.update("Failed to format code", 3)

def manage_style_guide(ui) -> None:
    """Manage style guide rules and enforcement."""
    while True:
        ui.print_header(
            "Style Guide",
            "Manage Code Style Rules"
        )

        menu_items = [
            MenuItem(
                key='check',
                label='Check Style',
                description='Check style guide violations',
                icon='🔍',
                shortcut='c'
            ),
            MenuItem(
                key='enforce',
                label='Enforce Style',
                description='Apply style guide rules',
                icon='✓',
                shortcut='e'
            ),
            MenuItem(
                key='back',
                label='Back to Code Quality Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'check':
            violations = ui.project.get_style_guide_violations()
            if violations:
                print("\nStyle Guide Violations:")
                for violation in violations:
                    print(f"- {violation.get('message', 'Unknown violation')}")
                print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
                input()
            else:
                ui.status_bar.update("No style guide violations found", 3)
        elif choice == 'enforce':
            if ui.project.enforce_style_guide():
                ui.status_bar.update("Style guide rules enforced successfully", 3)
            else:
                ui.status_bar.update("Failed to enforce style guide rules", 3)

def format_code(ui) -> None:
    """Format code files and directories."""
    while True:
        ui.print_header(
            "Format Code",
            "Format Files and Directories"
        )

        menu_items = [
            MenuItem(
                key='file',
                label='Format File',
                description='Format a specific file',
                icon='📄',
                shortcut='f'
            ),
            MenuItem(
                key='dir',
                label='Format Directory',
                description='Format entire directory',
                icon='📁',
                shortcut='d'
            ),
            MenuItem(
                key='config',
                label='Formatting Config',
                description='View/update formatting config',
                icon='⚙️',
                shortcut='c'
            ),
            MenuItem(
                key='back',
                label='Back to Code Quality Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'file':
            file_path = ui.get_input("File path to format", required=True)
            if ui.project.format_file(file_path):
                ui.status_bar.update("File formatted successfully", 3)
            else:
                ui.status_bar.update("Failed to format file", 3)
        elif choice == 'dir':
            directory = ui.get_input("Directory path to format", required=True)
            if ui.project.format_directory(directory):
                ui.status_bar.update("Directory formatted successfully", 3)
            else:
                ui.status_bar.update("Failed to format directory", 3)
        elif choice == 'config':
            manage_formatting_config(ui)

def manage_formatting_config(ui) -> None:
    """View and update formatting configuration."""
    while True:
        ui.print_header(
            "Formatting Configuration",
            "View and Update Settings"
        )

        config = ui.project.get_formatting_config()
        print("\nCurrent Configuration:")
        for section, settings in config.items():
            print(f"\n{section.upper()}:")
            for key, value in settings.items():
                print(f"  {key}: {value}")

        menu_items = [
            MenuItem(
                key='update',
                label='Update Config',
                description='Update formatting settings',
                icon='✏️',
                shortcut='u'
            ),
            MenuItem(
                key='back',
                label='Back to Format Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'update':
            new_config = {}
            print("\nEnter new configuration values (press Enter to keep current):")
            for section, settings in config.items():
                new_config[section] = {}
                for key, value in settings.items():
                    new_value = ui.get_input(f"{section}.{key} [{value}]")
                    if new_value:
                        new_config[section][key] = new_value
                    else:
                        new_config[section][key] = value

            if ui.project.update_formatting_config(new_config):
                ui.status_bar.update("Configuration updated successfully", 3)
            else:
                ui.status_bar.update("Failed to update configuration", 3)

def generate_quality_report(ui) -> None:
    """Generate and display code quality report."""
    report = ui.project.get_code_quality_report()
    if not report:
        ui.status_bar.update("Failed to generate quality report", 3)
        return

    print("\nCode Quality Report")
    print("==================")

    if report.get('eslint_issues'):
        print("\nESLint Issues:")
        for issue in report['eslint_issues']:
            print(f"- {issue}")

    if report.get('prettier_issues'):
        print("\nPrettier Issues:")
        for issue in report['prettier_issues']:
            print(f"- {issue}")

    if report.get('style_violations'):
        print("\nStyle Guide Violations:")
        for violation in report['style_violations']:
            print(f"- {violation}")

    if report.get('summary'):
        print("\nSummary:")
        for key, value in report['summary'].items():
            print(f"{key}: {value}")

    print(f"\n{ui.theme.COLORS['INFO']}Press Enter to continue...{ui.theme.COLORS['ENDC']}")
    input()
