"""Database menu implementation."""

from typing import List
from pathlib import Path
from ..models.menu_item import MenuItem
from ..project.database_manager import DatabaseManager

class DatabaseMenu:
    """Database tools menu."""

    def __init__(self, ui, project_manager):
        """Initialize database menu.

        Args:
            ui: UI instance for interaction
            project_manager: Project manager instance
        """
        self.ui = ui
        self.project_manager = project_manager
        self.db_manager = DatabaseManager(project_manager.project_root)

    def get_menu_items(self) -> List[MenuItem]:
        """Get database menu items.

        Returns:
            List of menu items
        """
        return [
            MenuItem(
                key="schema",
                label="Schema Management",
                description="Manage database schemas and migrations",
                icon="📊",
                handler=self.handle_schema_management
            ),
            MenuItem(
                key="backup",
                label="Backup/Restore",
                description="Backup and restore database",
                icon="💾",
                handler=self.handle_backup_restore
            ),
            MenuItem(
                key="data",
                label="Data Management",
                description="Import, export and clean data",
                icon="📋",
                handler=self.handle_data_management
            ),
            MenuItem(
                key="seed",
                label="Data Seeding",
                description="Seed database with initial data",
                icon="🌱",
                handler=self.handle_data_seeding
            )
        ]

    def handle_schema_management(self) -> None:
        """Handle schema management operations."""
        while True:
            self.ui.print_header(
                "Schema Management",
                "Manage database schemas and migrations"
            )

            options = [
                MenuItem(
                    key="validate",
                    label="Validate Schema",
                    description="Validate database schema against definition",
                    handler=self._validate_schema
                ),
                MenuItem(
                    key="back",
                    label="Back",
                    description="Return to database menu",
                    handler=lambda: True
                )
            ]

            self.ui.print_menu(options)
            choice = self.ui.get_input("Select an option", options)

            if choice == "back" or choice():
                break

    def handle_backup_restore(self) -> None:
        """Handle backup and restore operations."""
        while True:
            self.ui.print_header(
                "Backup/Restore",
                "Backup and restore database"
            )

            options = [
                MenuItem(
                    key="backup",
                    label="Create Backup",
                    description="Create database backup",
                    handler=self._create_backup
                ),
                MenuItem(
                    key="restore",
                    label="Restore Backup",
                    description="Restore database from backup",
                    handler=self._restore_backup
                ),
                MenuItem(
                    key="back",
                    label="Back",
                    description="Return to database menu",
                    handler=lambda: True
                )
            ]

            self.ui.print_menu(options)
            choice = self.ui.get_input("Select an option", options)

            if choice == "back" or choice():
                break

    def handle_data_management(self) -> None:
        """Handle data management operations."""
        while True:
            self.ui.print_header(
                "Data Management",
                "Import, export and clean data"
            )

            options = [
                MenuItem(
                    key="import",
                    label="Import Data",
                    description="Import data from file",
                    handler=self._import_data
                ),
                MenuItem(
                    key="export",
                    label="Export Data",
                    description="Export data to file",
                    handler=self._export_data
                ),
                MenuItem(
                    key="cleanup",
                    label="Clean Data",
                    description="Clean up data based on conditions",
                    handler=self._cleanup_data
                ),
                MenuItem(
                    key="back",
                    label="Back",
                    description="Return to database menu",
                    handler=lambda: True
                )
            ]

            self.ui.print_menu(options)
            choice = self.ui.get_input("Select an option", options)

            if choice == "back" or choice():
                break

    def handle_data_seeding(self) -> None:
        """Handle data seeding operations."""
        while True:
            self.ui.print_header(
                "Data Seeding",
                "Seed database with initial data"
            )

            options = [
                MenuItem(
                    key="seed",
                    label="Seed Database",
                    description="Seed database with data from file",
                    handler=self._seed_data
                ),
                MenuItem(
                    key="back",
                    label="Back",
                    description="Return to database menu",
                    handler=lambda: True
                )
            ]

            self.ui.print_menu(options)
            choice = self.ui.get_input("Select an option", options)

            if choice == "back" or choice():
                break

    def _validate_schema(self) -> bool:
        """Validate database schema."""
        db_name = self.ui.get_input("Enter database name")
        schema_path = self.ui.get_input("Enter schema definition file path")

        try:
            errors = self.db_manager.validate_schema(db_name, schema_path)
            if not errors:
                self.ui.print_success("Schema validation passed")
            else:
                self.ui.print_error("Schema validation failed:")
                for error in errors:
                    self.ui.print_error(f"- {error}")
        except Exception as e:
            self.ui.print_error(f"Error validating schema: {str(e)}")

        return False

    def _create_backup(self) -> bool:
        """Create database backup."""
        db_name = self.ui.get_input("Enter database name")

        try:
            backup_path = self.db_manager.create_backup(db_name)
            self.ui.print_success(f"Backup created at: {backup_path}")
        except Exception as e:
            self.ui.print_error(f"Error creating backup: {str(e)}")

        return False

    def _restore_backup(self) -> bool:
        """Restore database from backup."""
        backup_path = self.ui.get_input("Enter backup file path")
        db_name = self.ui.get_input("Enter target database name")

        try:
            self.db_manager.restore_backup(backup_path, db_name)
            self.ui.print_success("Database restored successfully")
        except Exception as e:
            self.ui.print_error(f"Error restoring backup: {str(e)}")

        return False

    def _import_data(self) -> bool:
        """Import data from file."""
        db_name = self.ui.get_input("Enter database name")
        data_file = self.ui.get_input("Enter data file path (CSV/JSON)")
        table = self.ui.get_input("Enter target table name")

        try:
            self.db_manager.import_data(db_name, data_file, table)
            self.ui.print_success("Data imported successfully")
        except Exception as e:
            self.ui.print_error(f"Error importing data: {str(e)}")

        return False

    def _export_data(self) -> bool:
        """Export data to file."""
        db_name = self.ui.get_input("Enter database name")
        table = self.ui.get_input("Enter source table name")
        output_file = self.ui.get_input("Enter output file path (CSV/JSON)")

        try:
            self.db_manager.export_data(db_name, table, output_file)
            self.ui.print_success("Data exported successfully")
        except Exception as e:
            self.ui.print_error(f"Error exporting data: {str(e)}")

        return False

    def _cleanup_data(self) -> bool:
        """Clean up data based on conditions."""
        db_name = self.ui.get_input("Enter database name")
        table = self.ui.get_input("Enter table name")
        conditions_str = self.ui.get_input("Enter conditions (JSON format)")

        try:
            import json
            conditions = json.loads(conditions_str)
            rows_affected = self.db_manager.cleanup_data(db_name, table, conditions)
            self.ui.print_success(f"Cleaned up {rows_affected} rows")
        except Exception as e:
            self.ui.print_error(f"Error cleaning up data: {str(e)}")

        return False

    def _seed_data(self) -> bool:
        """Seed database with data."""
        db_name = self.ui.get_input("Enter database name")
        seed_file = self.ui.get_input("Enter seed file path")

        try:
            self.db_manager.seed_data(db_name, seed_file)
            self.ui.print_success("Database seeded successfully")
        except Exception as e:
            self.ui.print_error(f"Error seeding database: {str(e)}")

        return False
