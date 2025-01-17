# HelloWorldGitHub CLI

A sophisticated CLI tool for managing the HelloWorldGitHub Astro.js project with integrated MCP tools.

## Project Structure

```
cli/
├── __init__.py          # Package initialization
├── __main__.py          # Main entry point
├── models/              # Data models
│   ├── __init__.py
│   └── menu_item.py     # MenuItem data class
├── menus/               # Menu implementations
│   ├── __init__.py
│   ├── main_menu.py     # Main menu
│   ├── development_menu.py
│   ├── testing_menu.py
│   ├── github_menu.py
│   ├── mcp_menu.py
│   └── project_menu.py
├── project/             # Project management
│   ├── __init__.py
│   └── project_manager.py
├── theme/               # Theme configuration
│   ├── __init__.py
│   └── theme.py
└── ui/                  # User interface
    ├── __init__.py
    ├── terminal.py      # Terminal UI implementation
    └── status_bar.py    # Status bar component
```

## Features

- Beautiful terminal UI with colors and icons
- Modular and extensible architecture
- Integrated project management tools
- Development server and build management
- Testing and coverage tools
- GitHub Pages deployment
- MCP tools integration
- Project-specific utilities

## Usage

Run the CLI:

```bash
./cli.py
```

## Navigation

- Use number keys (1-9) to select menu items
- Use shortcuts shown in parentheses for quick access
- Press 'b' to go back to previous menu
- Press 'h' for help
- Press 'x' to exit

## Menus

1. Development
   - Server options
   - Build options
   - Asset management

2. Testing
   - Unit testing
   - E2E testing
   - Coverage options

3. GitHub & Deployment
   - GitHub Pages
   - Repository management
   - GitHub Actions

4. MCP Tools
   - Code quality
   - Optimization
   - Project tools

5. Project Tools
   - Compound management
   - Page management
   - Component tools

## Development

The CLI is structured into modules for maintainability:

- `models/`: Data structures and types
- `menus/`: Menu implementations and navigation
- `project/`: Project-specific operations
- `theme/`: UI theme configuration
- `ui/`: Terminal interface components

Each module is self-contained and follows Python best practices.
