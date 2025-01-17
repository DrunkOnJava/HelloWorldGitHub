"""Deployment management menu implementation."""
import os
import json
from typing import Any, Dict, List
from ..models.menu_item import MenuItem
from ..project.deployment_manager import DeploymentManager

def show_deployment_menu(ui, project_manager) -> None:
    """Show deployment management menu."""
    deployment_manager = DeploymentManager(project_manager.project_root)

    while True:
        ui.clear()
        ui.print_title("Deployment Management")

        menu_items = [
            MenuItem(
                label="Environment Management",
                description="Manage deployment environments",
                icon="🌍",
                handler=lambda: show_environment_menu(ui, deployment_manager)
            ),
            MenuItem(
                label="Release Management",
                description="Create and manage releases",
                icon="📦",
                handler=lambda: show_release_menu(ui, deployment_manager)
            ),
            MenuItem(
                label="Backup & Rollback",
                description="Manage deployment backups and rollbacks",
                icon="⏮️",
                handler=lambda: show_backup_menu(ui, deployment_manager)
            ),
            MenuItem(
                label="Back to Main Menu",
                description="Return to main menu",
                icon="⬅️",
                handler=lambda: "exit"
            )
        ]

        choice = ui.show_menu_and_get_choice(menu_items)
        if choice == "exit":
            break

def show_environment_menu(ui, deployment_manager: DeploymentManager) -> None:
    """Show environment management menu."""
    while True:
        ui.clear()
        ui.print_title("Environment Management")

        menu_items = [
            MenuItem(
                label="List Environments",
                description="Show all configured environments",
                icon="📋",
                handler=lambda: list_environments(ui, deployment_manager)
            ),
            MenuItem(
                label="Create Environment",
                description="Create a new deployment environment",
                icon="➕",
                handler=lambda: create_environment(ui, deployment_manager)
            ),
            MenuItem(
                label="Edit Environment",
                description="Modify environment configuration",
                icon="✏️",
                handler=lambda: edit_environment(ui, deployment_manager)
            ),
            MenuItem(
                label="Back",
                description="Return to deployment menu",
                icon="⬅️",
                handler=lambda: "exit"
            )
        ]

        choice = ui.show_menu_and_get_choice(menu_items)
        if choice == "exit":
            break

def show_release_menu(ui, deployment_manager: DeploymentManager) -> None:
    """Show release management menu."""
    while True:
        ui.clear()
        ui.print_title("Release Management")

        menu_items = [
            MenuItem(
                label="Create Release",
                description="Create a new release",
                icon="📦",
                handler=lambda: create_release(ui, deployment_manager)
            ),
            MenuItem(
                label="Bump Version",
                description="Bump project version",
                icon="⬆️",
                handler=lambda: bump_version(ui, deployment_manager)
            ),
            MenuItem(
                label="View Changelog",
                description="View project changelog",
                icon="📄",
                handler=lambda: view_changelog(ui, deployment_manager)
            ),
            MenuItem(
                label="Back",
                description="Return to deployment menu",
                icon="⬅️",
                handler=lambda: "exit"
            )
        ]

        choice = ui.show_menu_and_get_choice(menu_items)
        if choice == "exit":
            break

def show_backup_menu(ui, deployment_manager: DeploymentManager) -> None:
    """Show backup and rollback menu."""
    while True:
        ui.clear()
        ui.print_title("Backup & Rollback")

        menu_items = [
            MenuItem(
                label="Create Backup",
                description="Create deployment backup",
                icon="💾",
                handler=lambda: create_backup(ui, deployment_manager)
            ),
            MenuItem(
                label="List Backups",
                description="Show available backups",
                icon="📋",
                handler=lambda: list_backups(ui, deployment_manager)
            ),
            MenuItem(
                label="Rollback Deployment",
                description="Rollback to previous deployment",
                icon="⏮️",
                handler=lambda: rollback_deployment(ui, deployment_manager)
            ),
            MenuItem(
                label="Back",
                description="Return to deployment menu",
                icon="⬅️",
                handler=lambda: "exit"
            )
        ]

        choice = ui.show_menu_and_get_choice(menu_items)
        if choice == "exit":
            break

# Environment Management Functions
def list_environments(ui, deployment_manager: DeploymentManager) -> None:
    """List all configured environments."""
    ui.clear()
    ui.print_title("Configured Environments")

    for env in ["development", "staging", "production"]:
        config = deployment_manager.get_environment(env)
        if config:
            ui.print_info(f"\n{config['name'].upper()}")
            ui.print_info(f"URL: {config['url']}")
            ui.print_info(f"Branch: {config['branch']}")
            ui.print_info(f"Auto Deploy: {'Yes' if config['auto_deploy'] else 'No'}")
            ui.print_info(f"Require Approval: {'Yes' if config['require_approval'] else 'No'}")

    ui.wait_for_enter()

def create_environment(ui, deployment_manager: DeploymentManager) -> None:
    """Create a new environment."""
    ui.clear()
    ui.print_title("Create Environment")

    name = ui.get_input("Environment Name: ")
    url = ui.get_input("Environment URL: ")
    branch = ui.get_input("Git Branch: ")
    auto_deploy = ui.get_yes_no("Enable Auto Deploy?")
    require_approval = ui.get_yes_no("Require Approval?")

    config = {
        "url": url,
        "branch": branch,
        "auto_deploy": auto_deploy,
        "require_approval": require_approval
    }

    deployment_manager.create_environment(name, config)
    ui.print_success(f"Environment '{name}' created successfully!")
    ui.wait_for_enter()

def edit_environment(ui, deployment_manager: DeploymentManager) -> None:
    """Edit environment configuration."""
    ui.clear()
    ui.print_title("Edit Environment")

    name = ui.get_input("Environment to Edit: ")
    config = deployment_manager.get_environment(name)

    if not config:
        ui.print_error(f"Environment '{name}' not found!")
        ui.wait_for_enter()
        return

    url = ui.get_input("Environment URL: ", default=config["url"])
    branch = ui.get_input("Git Branch: ", default=config["branch"])
    auto_deploy = ui.get_yes_no("Enable Auto Deploy?", default=config["auto_deploy"])
    require_approval = ui.get_yes_no("Require Approval?", default=config["require_approval"])

    new_config = {
        "url": url,
        "branch": branch,
        "auto_deploy": auto_deploy,
        "require_approval": require_approval
    }

    deployment_manager.create_environment(name, new_config)
    ui.print_success(f"Environment '{name}' updated successfully!")
    ui.wait_for_enter()

# Release Management Functions
def create_release(ui, deployment_manager: DeploymentManager) -> None:
    """Create a new release."""
    ui.clear()
    ui.print_title("Create Release")

    version = ui.get_input("Release Version: ")
    changes = []

    while True:
        change = ui.get_input("Change (empty to finish): ")
        if not change:
            break
        changes.append(change)

    release = deployment_manager.create_release(version, changes)
    ui.print_success(f"Release {version} created successfully!")
    ui.wait_for_enter()

def bump_version(ui, deployment_manager: DeploymentManager) -> None:
    """Bump project version."""
    ui.clear()
    ui.print_title("Bump Version")

    bump_type = ui.get_choice(
        "Select version bump type:",
        choices=["major", "minor", "patch"],
        default="patch"
    )

    new_version = deployment_manager.bump_version(bump_type)
    ui.print_success(f"Version bumped to {new_version}")
    ui.wait_for_enter()

def view_changelog(ui, deployment_manager: DeploymentManager) -> None:
    """View project changelog."""
    ui.clear()
    ui.print_title("Changelog")

    changelog_path = os.path.join(deployment_manager.project_root, "CHANGELOG.md")
    if os.path.exists(changelog_path):
        with open(changelog_path, "r") as f:
            ui.print_info(f.read())
    else:
        ui.print_warning("No changelog found.")

    ui.wait_for_enter()

# Backup and Rollback Functions
def create_backup(ui, deployment_manager: DeploymentManager) -> None:
    """Create deployment backup."""
    ui.clear()
    ui.print_title("Create Backup")

    environment = ui.get_input("Environment to backup: ")
    backup_id = deployment_manager.create_backup(environment)

    ui.print_success(f"Backup created successfully! Backup ID: {backup_id}")
    ui.wait_for_enter()

def list_backups(ui, deployment_manager: DeploymentManager) -> None:
    """List available backups."""
    ui.clear()
    ui.print_title("Available Backups")

    backup_dir = os.path.join(deployment_manager.deployments_dir, "backups")
    if os.path.exists(backup_dir):
        for backup_id in os.listdir(backup_dir):
            metadata_file = os.path.join(backup_dir, backup_id, "metadata.json")
            if os.path.exists(metadata_file):
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    ui.print_info(f"\nBackup ID: {metadata['id']}")
                    ui.print_info(f"Environment: {metadata['environment']}")
                    ui.print_info(f"Created: {metadata['created_at']}")
                    ui.print_info(f"Git Commit: {metadata['git_commit']}")
    else:
        ui.print_warning("No backups found.")

    ui.wait_for_enter()

def rollback_deployment(ui, deployment_manager: DeploymentManager) -> None:
    """Rollback to previous deployment."""
    ui.clear()
    ui.print_title("Rollback Deployment")

    environment = ui.get_input("Environment to rollback: ")
    backup_id = ui.get_input("Backup ID to restore: ")

    if deployment_manager.rollback(environment, backup_id):
        ui.print_success("Rollback completed successfully!")
    else:
        ui.print_error("Rollback failed. Backup not found.")

    ui.wait_for_enter()
