#!/usr/bin/env venv/bin/python3
"""CLI wrapper script for HelloWorldGitHub CLI."""

import sys
import os

# Add the parent directory to Python path so cli package can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cli.__main__ import main

if __name__ == "__main__":
    main()
