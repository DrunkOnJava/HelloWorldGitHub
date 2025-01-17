"""Utility functions for Git operations."""

import subprocess
from typing import Dict, Any, Optional, Tuple

class GitCommandError(Exception):
    """Custom exception for Git command failures."""
    pass

def execute_git_command(
    command: str,
    cwd: str,
    input_data: Optional[str] = None,
    capture_output: bool = True,
    check: bool = True
) -> Tuple[str, str]:
    """Execute a Git command and handle common error cases.

    Args:
        command: The command to execute
        cwd: Working directory for command execution
        input_data: Optional input data for the command
        capture_output: Whether to capture command output
        check: Whether to check for command success

    Returns:
        Tuple of (stdout, stderr)

    Raises:
        GitCommandError: If command execution fails
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            input=input_data,
            check=check
        )
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        raise GitCommandError(f"Git command failed: {e.stderr}")
    except Exception as e:
        raise GitCommandError(f"Error executing git command: {str(e)}")

def format_error_message(error: str, ui_theme: Dict[str, str]) -> str:
    """Format error message with color theme.

    Args:
        error: Error message to format
        ui_theme: UI theme colors dictionary

    Returns:
        Formatted error message with color
    """
    return f"\n{ui_theme['ERROR']}{error}{ui_theme['ENDC']}"

def format_success_message(message: str, ui_theme: Dict[str, str]) -> str:
    """Format success message with color theme.

    Args:
        message: Success message to format
        ui_theme: UI theme colors dictionary

    Returns:
        Formatted success message with color
    """
    return f"\n{ui_theme['SUCCESS']}{message}{ui_theme['ENDC']}"
