"""Database management functionality."""

import os
import json
import sqlite3
from datetime import datetime
from typing import Optional, Dict, List, Any
from pathlib import Path

class DatabaseManager:
    """Manages database operations and utilities."""

    def __init__(self, project_root: str):
        """Initialize database manager.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.db_dir = os.path.join(project_root, 'db')
        self._ensure_db_directory()

    def _ensure_db_directory(self) -> None:
        """Ensure database directory exists."""
        os.makedirs(self.db_dir, exist_ok=True)

    def create_backup(self, db_name: str) -> str:
        """Create backup of database.

        Args:
            db_name: Name of database to backup

        Returns:
            Path to backup file
        """
        source = os.path.join(self.db_dir, f"{db_name}.db")
        if not os.path.exists(source):
            raise FileNotFoundError(f"Database {db_name} not found")

        backup_dir = os.path.join(self.db_dir, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f"{db_name}_{timestamp}.db")

        with sqlite3.connect(source) as src_conn:
            with sqlite3.connect(backup_path) as dst_conn:
                src_conn.backup(dst_conn)

        return backup_path

    def restore_backup(self, backup_path: str, db_name: str) -> None:
        """Restore database from backup.

        Args:
            backup_path: Path to backup file
            db_name: Name of database to restore to
        """
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        target = os.path.join(self.db_dir, f"{db_name}.db")

        with sqlite3.connect(backup_path) as src_conn:
            with sqlite3.connect(target) as dst_conn:
                src_conn.backup(dst_conn)

    def validate_schema(self, db_name: str, schema_path: str) -> List[str]:
        """Validate database schema against definition.

        Args:
            db_name: Name of database to validate
            schema_path: Path to schema definition file

        Returns:
            List of validation errors, empty if valid
        """
        db_path = os.path.join(self.db_dir, f"{db_name}.db")
        if not os.path.exists(db_path):
            return ["Database does not exist"]

        if not os.path.exists(schema_path):
            return ["Schema definition file not found"]

        try:
            with open(schema_path) as f:
                schema = json.load(f)
        except json.JSONDecodeError:
            return ["Invalid schema definition file"]

        errors = []
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Get existing tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = {row[0] for row in cursor.fetchall()}

            # Check each table in schema
            for table_name, table_def in schema.items():
                if table_name not in existing_tables:
                    errors.append(f"Missing table: {table_name}")
                    continue

                # Get column info
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = {row[1]: row for row in cursor.fetchall()}

                # Check columns
                for col_name, col_def in table_def["columns"].items():
                    if col_name not in columns:
                        errors.append(f"Missing column: {table_name}.{col_name}")
                        continue

                    col_info = columns[col_name]
                    if col_def["type"].upper() != col_info[2].upper():
                        errors.append(
                            f"Type mismatch for {table_name}.{col_name}: "
                            f"expected {col_def['type']}, got {col_info[2]}"
                        )

        return errors

    def import_data(self, db_name: str, data_file: str, table: str) -> None:
        """Import data from file into database table.

        Args:
            db_name: Target database name
            data_file: Path to data file (CSV/JSON)
            table: Target table name
        """
        db_path = os.path.join(self.db_dir, f"{db_name}.db")
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database {db_name} not found")

        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file not found: {data_file}")

        ext = os.path.splitext(data_file)[1].lower()

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            if ext == '.json':
                with open(data_file) as f:
                    data = json.load(f)
                if not data:
                    return

                # Get column names from first row
                columns = list(data[0].keys())
                placeholders = ','.join(['?' for _ in columns])

                # Insert data
                cursor.executemany(
                    f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})",
                    [tuple(row[col] for col in columns) for row in data]
                )

            elif ext == '.csv':
                import csv
                with open(data_file) as f:
                    reader = csv.DictReader(f)
                    if not reader.fieldnames:
                        return

                    columns = reader.fieldnames
                    placeholders = ','.join(['?' for _ in columns])

                    cursor.executemany(
                        f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})",
                        [tuple(row[col] for col in columns) for row in reader]
                    )
            else:
                raise ValueError("Unsupported file format")

            conn.commit()

    def export_data(self, db_name: str, table: str, output_file: str) -> None:
        """Export table data to file.

        Args:
            db_name: Source database name
            table: Source table name
            output_file: Target output file (CSV/JSON)
        """
        db_path = os.path.join(self.db_dir, f"{db_name}.db")
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database {db_name} not found")

        ext = os.path.splitext(output_file)[1].lower()

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Get column names
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]

            # Get data
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            if ext == '.json':
                data = [
                    {col: value for col, value in zip(columns, row)}
                    for row in rows
                ]
                with open(output_file, 'w') as f:
                    json.dump(data, f, indent=2)

            elif ext == '.csv':
                import csv
                with open(output_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)
                    writer.writerows(rows)
            else:
                raise ValueError("Unsupported file format")

    def cleanup_data(self, db_name: str, table: str, conditions: Dict[str, Any]) -> int:
        """Clean up data in table based on conditions.

        Args:
            db_name: Target database name
            table: Target table name
            conditions: Cleanup conditions

        Returns:
            Number of rows affected
        """
        db_path = os.path.join(self.db_dir, f"{db_name}.db")
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database {db_name} not found")

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            where_clauses = []
            params = []

            for column, condition in conditions.items():
                if isinstance(condition, (list, tuple)):
                    where_clauses.append(f"{column} IN ({','.join(['?' for _ in condition])})")
                    params.extend(condition)
                else:
                    where_clauses.append(f"{column} = ?")
                    params.append(condition)

            where_sql = ' AND '.join(where_clauses)

            cursor.execute(f"DELETE FROM {table} WHERE {where_sql}", params)
            conn.commit()

            return cursor.rowcount

    def seed_data(self, db_name: str, seed_file: str) -> None:
        """Seed database with initial data.

        Args:
            db_name: Target database name
            seed_file: Path to seed data file
        """
        db_path = os.path.join(self.db_dir, f"{db_name}.db")
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database {db_name} not found")

        if not os.path.exists(seed_file):
            raise FileNotFoundError(f"Seed file not found: {seed_file}")

        try:
            with open(seed_file) as f:
                seed_data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid seed file format")

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            for table_name, rows in seed_data.items():
                if not rows:
                    continue

                columns = list(rows[0].keys())
                placeholders = ','.join(['?' for _ in columns])

                cursor.executemany(
                    f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})",
                    [tuple(row[col] for col in columns) for row in rows]
                )

            conn.commit()
