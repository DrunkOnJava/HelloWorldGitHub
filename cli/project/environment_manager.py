"""Environment variable management functionality."""

import os
from typing import Dict, List, Optional
from pathlib import Path
import json
import re

class EnvironmentManager:
    """Handles environment variable management."""
    def __init__(self, ui):
        self.ui = ui
        self.env_file = ".env"
        self.env_example_file = ".env.example"

    def get_environment_variables(self) -> Dict[str, str]:
        """Get current environment variables."""
        try:
            env_vars = {}
            if os.path.exists(self.env_file):
                with open(self.env_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            key, value = line.split("=", 1)
                            env_vars[key.strip()] = value.strip()
            return env_vars
        except Exception as e:
            self.ui.status_bar.update(f"Error reading environment variables: {str(e)}", 3)
            return {}

    def add_environment_variable(self, key: str, value: str) -> bool:
        """Add new environment variable."""
        try:
            # Validate key format
            if not re.match(r"^[A-Z][A-Z0-9_]*$", key):
                raise ValueError("Invalid environment variable name format")

            # Read existing variables
            env_vars = self.get_environment_variables()

            # Add new variable
            env_vars[key] = value

            # Write back to file
            self._write_env_file(env_vars)

            # Update example file if it exists
            self._update_example_file(key)

            return True
        except Exception as e:
            self.ui.status_bar.update(f"Error adding environment variable: {str(e)}", 3)
            return False

    def update_environment_variable(self, key: str, value: str) -> bool:
        """Update existing environment variable."""
        try:
            env_vars = self.get_environment_variables()
            if key not in env_vars:
                raise ValueError(f"Environment variable {key} not found")

            env_vars[key] = value
            self._write_env_file(env_vars)
            return True
        except Exception as e:
            self.ui.status_bar.update(f"Error updating environment variable: {str(e)}", 3)
            return False

    def delete_environment_variable(self, key: str) -> bool:
        """Delete environment variable."""
        try:
            env_vars = self.get_environment_variables()
            if key not in env_vars:
                raise ValueError(f"Environment variable {key} not found")

            del env_vars[key]
            self._write_env_file(env_vars)
            return True
        except Exception as e:
            self.ui.status_bar.update(f"Error deleting environment variable: {str(e)}", 3)
            return False

    def validate_environment_config(self) -> List[str]:
        """Validate environment configuration."""
        issues = []
        try:
            # Check if .env file exists
            if not os.path.exists(self.env_file):
                issues.append("Missing .env file")
                return issues

            # Check if .env.example exists
            if not os.path.exists(self.env_example_file):
                issues.append("Missing .env.example file")

            # Read both files
            env_vars = self.get_environment_variables()
            example_vars = self._read_example_file()

            # Check for missing required variables
            for key in example_vars:
                if key not in env_vars:
                    issues.append(f"Missing required environment variable: {key}")

            # Check for invalid formats
            for key, value in env_vars.items():
                if not re.match(r"^[A-Z][A-Z0-9_]*$", key):
                    issues.append(f"Invalid environment variable name format: {key}")
                if not value:
                    issues.append(f"Empty value for environment variable: {key}")

            return issues
        except Exception as e:
            self.ui.status_bar.update(f"Error validating environment config: {str(e)}", 3)
            return [str(e)]

    def _write_env_file(self, env_vars: Dict[str, str]) -> None:
        """Write environment variables to .env file."""
        with open(self.env_file, "w") as f:
            for key, value in sorted(env_vars.items()):
                f.write(f"{key}={value}\n")

    def _read_example_file(self) -> Dict[str, str]:
        """Read variables from .env.example file."""
        example_vars = {}
        if os.path.exists(self.env_example_file):
            with open(self.env_example_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        key = line.split("=", 1)[0].strip()
                        example_vars[key] = ""
        return example_vars

    def _update_example_file(self, key: str) -> None:
        """Update .env.example file with new variable."""
        if os.path.exists(self.env_example_file):
            example_vars = self._read_example_file()
            if key not in example_vars:
                with open(self.env_example_file, "a") as f:
                    f.write(f"\n{key}=\n")
