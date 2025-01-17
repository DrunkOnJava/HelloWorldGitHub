"""GitHub and deployment menu implementation."""

from ..models.menu_item import MenuItem

def show_github_menu(ui) -> None:
    """GitHub and deployment menu implementation with submenus."""
    while True:
        ui.print_header(
            "GitHub & Deployment",
            "Manage GitHub Pages and Deployments"
        )

        menu_items = [
            MenuItem(
                key='pages',
                label='GitHub Pages',
                description='GitHub Pages deployment options',
                icon='🌐',
                shortcut='p'
            ),
            MenuItem(
                key='repo',
                label='Repository Management',
                description='Manage GitHub repository',
                icon='📦',
                shortcut='r'
            ),
            MenuItem(
                key='actions',
                label='GitHub Actions',
                description='Manage CI/CD workflows',
                icon='⚙️',
                shortcut='a'
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
        elif choice == 'pages':
            show_github_pages_submenu(ui)
        elif choice == 'repo':
            show_repo_management_submenu(ui)
        elif choice == 'actions':
            show_github_actions_submenu(ui)

def show_github_pages_submenu(ui) -> None:
    """GitHub Pages submenu."""
    while True:
        ui.print_header(
            "GitHub Pages",
            "Deployment and Optimization"
        )

        menu_items = [
            MenuItem(
                key='deploy',
                label='Deploy to Pages',
                description='Build and deploy to GitHub Pages',
                icon='🚀',
                shortcut='d'
            ),
            MenuItem(
                key='optimize',
                label='Optimize for Pages',
                description='Run GitHub Pages optimization tools',
                icon='⚡',
                shortcut='o'
            ),
            MenuItem(
                key='preview',
                label='Preview Deployment',
                description='Preview the deployment locally',
                icon='👁️',
                shortcut='p'
            ),
            MenuItem(
                key='settings',
                label='Pages Settings',
                description='Configure GitHub Pages settings',
                icon='⚙️',
                shortcut='s'
            ),
            MenuItem(
                key='back',
                label='Back to GitHub Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'deploy':
            ui.project.run_npm_command('deploy')
        elif choice == 'optimize':
            ui.project.run_npm_command('optimize:pages')
        elif choice == 'preview':
            ui.project.run_npm_command('preview:deploy')
        elif choice == 'settings':
            if ui.project.configure_pages_settings():
                ui.status_bar.update("GitHub Pages settings updated successfully", 2)
            else:
                ui.status_bar.update("Failed to update GitHub Pages settings", 2, error=True)

def show_repo_management_submenu(ui) -> None:
    """Repository management submenu."""
    while True:
        ui.print_header(
            "Repository Management",
            "GitHub Repository Tools"
        )

        menu_items = [
            MenuItem(
                key='status',
                label='Repository Status',
                description='View repository status and info',
                icon='📊',
                shortcut='s'
            ),
            MenuItem(
                key='branch',
                label='Branch Management',
                description='Manage Git branches',
                icon='🌿',
                shortcut='b'
            ),
            MenuItem(
                key='sync',
                label='Sync Repository',
                description='Sync with remote repository',
                icon='🔄',
                shortcut='y'
            ),
            MenuItem(
                key='issues',
                label='Issue Management',
                description='Manage GitHub issues',
                icon='🎫',
                shortcut='i'
            ),
            MenuItem(
                key='back',
                label='Back to GitHub Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'status':
            status = ui.project.get_repo_status()
            if status:
                ui.print_header("Repository Status", "Current Git Status")
                print(f"\nCurrent Branch: {status['branch']}")
                print(f"Changes: {status['changes']} file(s) modified")
                if status['changed_files']:
                    print("\nModified Files:")
                    for file in status['changed_files']:
                        print(f"  {file}")
                if status['remotes']:
                    print("\nRemotes:")
                    for name, url in status['remotes'].items():
                        print(f"  {name}: {url}")
                ui.status_bar.update("Repository status retrieved successfully", 2)
            else:
                ui.status_bar.update("Failed to get repository status", 2, error=True)
        elif choice == 'branch':
            branch_submenu(ui)
        elif choice == 'sync':
            if ui.project.sync_repository():
                ui.status_bar.update("Repository synced successfully", 2)
            else:
                ui.status_bar.update("Failed to sync repository", 2, error=True)
        elif choice == 'issues':
            issue_submenu(ui)

def branch_submenu(ui) -> None:
    """Branch management submenu."""
    while True:
        ui.print_header(
            "Branch Management",
            "Manage Git Branches"
        )

        menu_items = [
            MenuItem(
                key='create',
                label='Create Branch',
                description='Create a new branch',
                icon='➕',
                shortcut='c'
            ),
            MenuItem(
                key='switch',
                label='Switch Branch',
                description='Switch to another branch',
                icon='🔄',
                shortcut='s'
            ),
            MenuItem(
                key='delete',
                label='Delete Branch',
                description='Delete a branch',
                icon='🗑️',
                shortcut='d'
            ),
            MenuItem(
                key='back',
                label='Back to Repository Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'create':
            branch_name = ui.get_input("Enter new branch name")
            if ui.project.manage_branches('create', branch_name):
                ui.status_bar.update(f"Created branch: {branch_name}", 2)
            else:
                ui.status_bar.update("Failed to create branch", 2, error=True)
        elif choice == 'switch':
            branch_name = ui.get_input("Enter branch name to switch to")
            if ui.project.manage_branches('switch', branch_name):
                ui.status_bar.update(f"Switched to branch: {branch_name}", 2)
            else:
                ui.status_bar.update("Failed to switch branch", 2, error=True)
        elif choice == 'delete':
            branch_name = ui.get_input("Enter branch name to delete")
            if ui.project.manage_branches('delete', branch_name):
                ui.status_bar.update(f"Deleted branch: {branch_name}", 2)
            else:
                ui.status_bar.update("Failed to delete branch", 2, error=True)

def issue_submenu(ui) -> None:
    """Issue management submenu."""
    while True:
        ui.print_header(
            "Issue Management",
            "Manage GitHub Issues"
        )

        menu_items = [
            MenuItem(
                key='list',
                label='List Issues',
                description='View all issues',
                icon='📋',
                shortcut='l'
            ),
            MenuItem(
                key='create',
                label='Create Issue',
                description='Create a new issue',
                icon='➕',
                shortcut='c'
            ),
            MenuItem(
                key='close',
                label='Close Issue',
                description='Close an existing issue',
                icon='✔️',
                shortcut='x'
            ),
            MenuItem(
                key='back',
                label='Back to Repository Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'list':
            if ui.project.manage_issues('list'):
                ui.status_bar.update("Issues listed successfully", 2)
            else:
                ui.status_bar.update("Failed to list issues", 2, error=True)
        elif choice == 'create':
            title = ui.get_input("Enter issue title")
            body = ui.get_input("Enter issue description")
            issue_data = {'title': title, 'body': body}
            if ui.project.manage_issues('create', issue_data):
                ui.status_bar.update("Issue created successfully", 2)
            else:
                ui.status_bar.update("Failed to create issue", 2, error=True)
        elif choice == 'close':
            issue_number = ui.get_input("Enter issue number to close")
            if ui.project.manage_issues('close', {'number': issue_number}):
                ui.status_bar.update(f"Closed issue #{issue_number}", 2)
            else:
                ui.status_bar.update("Failed to close issue", 2, error=True)

def secrets_submenu(ui) -> None:
    """GitHub Actions secrets management submenu."""
    while True:
        ui.print_header(
            "Secrets Management",
            "Manage GitHub Actions Secrets"
        )

        menu_items = [
            MenuItem(
                key='list',
                label='List Secrets',
                description='View all repository secrets',
                icon='📋',
                shortcut='l'
            ),
            MenuItem(
                key='add',
                label='Add Secret',
                description='Add a new secret',
                icon='➕',
                shortcut='a'
            ),
            MenuItem(
                key='update',
                label='Update Secret',
                description='Update an existing secret',
                icon='🔄',
                shortcut='u'
            ),
            MenuItem(
                key='delete',
                label='Delete Secret',
                description='Delete an existing secret',
                icon='🗑️',
                shortcut='d'
            ),
            MenuItem(
                key='back',
                label='Back to Actions Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'list':
            if ui.project.manage_secrets('list'):
                ui.status_bar.update("Secrets listed successfully", 2)
            else:
                ui.status_bar.update("Failed to list secrets", 2, error=True)
        elif choice == 'add':
            name = ui.get_input("Enter secret name")
            value = ui.get_input("Enter secret value", password=True)
            if ui.project.manage_secrets('create', {'name': name, 'value': value}):
                ui.status_bar.update(f"Secret '{name}' created successfully", 2)
            else:
                ui.status_bar.update("Failed to create secret", 2, error=True)
        elif choice == 'update':
            name = ui.get_input("Enter secret name to update")
            value = ui.get_input("Enter new secret value", password=True)
            if ui.project.manage_secrets('update', {'name': name, 'value': value}):
                ui.status_bar.update(f"Secret '{name}' updated successfully", 2)
            else:
                ui.status_bar.update("Failed to update secret", 2, error=True)
        elif choice == 'delete':
            name = ui.get_input("Enter secret name to delete")
            if ui.project.manage_secrets('delete', {'name': name}):
                ui.status_bar.update(f"Secret '{name}' deleted successfully", 2)
            else:
                ui.status_bar.update("Failed to delete secret", 2, error=True)

def show_github_actions_submenu(ui) -> None:
    """GitHub Actions submenu."""
    while True:
        ui.print_header(
            "GitHub Actions",
            "CI/CD Workflow Management"
        )

        menu_items = [
            MenuItem(
                key='workflows',
                label='View Workflows',
                description='List and manage workflows',
                icon='📋',
                shortcut='w'
            ),
            MenuItem(
                key='runs',
                label='Workflow Runs',
                description='View recent workflow runs',
                icon='🏃',
                shortcut='r'
            ),
            MenuItem(
                key='create',
                label='Create Workflow',
                description='Create new GitHub Action workflow',
                icon='➕',
                shortcut='c'
            ),
            MenuItem(
                key='secrets',
                label='Manage Secrets',
                description='Manage GitHub Actions secrets',
                icon='🔒',
                shortcut='s'
            ),
            MenuItem(
                key='back',
                label='Back to GitHub Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'workflows':
            if ui.project.manage_ci_pipeline('list'):
                ui.status_bar.update("Workflows listed successfully", 2)
            else:
                ui.status_bar.update("Failed to list workflows", 2, error=True)
        elif choice == 'runs':
            workflow = ui.get_input("Enter workflow name")
            if ui.project.manage_ci_pipeline('run', {'workflow': workflow}):
                ui.status_bar.update(f"Triggered workflow: {workflow}", 2)
            else:
                ui.status_bar.update("Failed to trigger workflow", 2, error=True)
        elif choice == 'create':
            name = ui.get_input("Enter workflow name")
            pipeline_data = {
                'name': name,
                'build': True,
                'test': True,
                'lint': True,
                'node_version': '18',
                'branches': ['main']
            }
            if ui.project.manage_ci_pipeline('create', pipeline_data):
                ui.status_bar.update(f"Created workflow: {name}", 2)
            else:
                ui.status_bar.update("Failed to create workflow", 2, error=True)
        elif choice == 'secrets':
            secrets_submenu(ui)
