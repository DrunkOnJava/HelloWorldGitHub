"""Bundle analysis and optimization functionality."""

from typing import List, Dict, Any, Optional

class BundleManager:
    """Handles bundle analysis and optimization."""
    def __init__(self, ui):
        self.ui = ui

    def analyze_bundle_size(self) -> bool:
        """Analyze bundle size and composition."""
        try:
            # Use webpack-bundle-analyzer
            command = "npx webpack-bundle-analyzer dist/stats.json"
            return self.ui.run_command(command)
        except Exception as e:
            self.ui.status_bar.update(f"Bundle analysis error: {str(e)}", 3)
            return False

    def analyze_dependencies(self) -> bool:
        """Analyze project dependencies."""
        try:
            # Use npm-check for dependency analysis
            command = "npx npm-check"
            return self.ui.run_command(command)
        except Exception as e:
            self.ui.status_bar.update(f"Dependency analysis error: {str(e)}", 3)
            return False

    def find_unused_code(self) -> bool:
        """Find unused code and imports."""
        try:
            # Use tree-shaking analysis
            command = "npx webpack --json > stats.json && npx webpack-unused -s stats.json"
            return self.ui.run_command(command)
        except Exception as e:
            self.ui.status_bar.update(f"Unused code analysis error: {str(e)}", 3)
            return False

    def optimize_bundle(self) -> bool:
        """Optimize bundle size."""
        try:
            # Run various optimization steps
            commands = [
                # Generate production build with optimizations
                "npm run build",
                # Analyze and remove unused code
                "npx webpack --optimize-minimize --json > stats.json",
                # Run compression
                "npx compression-webpack-plugin",
                # Generate report
                "npx webpack-bundle-analyzer stats.json"
            ]

            for command in commands:
                if not self.ui.run_command(command):
                    return False
            return True
        except Exception as e:
            self.ui.status_bar.update(f"Bundle optimization error: {str(e)}", 3)
            return False

    def get_bundle_stats(self) -> Optional[Dict[str, Any]]:
        """Get bundle statistics."""
        try:
            # Generate and read stats
            self.ui.run_command("npx webpack --json > stats.json")
            import json
            with open("stats.json", "r") as f:
                return json.load(f)
        except Exception as e:
            self.ui.status_bar.update(f"Error getting bundle stats: {str(e)}", 3)
            return None
