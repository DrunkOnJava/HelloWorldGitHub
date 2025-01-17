"""Logging menu implementation."""

from typing import List
from ..models.menu_item import MenuItem

class LoggingMenu:
    """Menu for logging and monitoring tools."""

    def __init__(self, ui, logging_manager):
        """Initialize logging menu.

        Args:
            ui: UI instance for terminal interaction
            logging_manager: LoggingManager instance
        """
        self.ui = ui
        self.logging_manager = logging_manager

    def get_menu_items(self) -> List[MenuItem]:
        """Get logging menu items.

        Returns:
            List of menu items
        """
        return [
            MenuItem(
                key="level",
                label="Configure Log Level",
                description="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
                handler=self._configure_log_level
            ),
            MenuItem(
                key="view",
                label="View Recent Logs",
                description="View the most recent log entries",
                handler=self._view_recent_logs
            ),
            MenuItem(
                key="analyze",
                label="Analyze Logs",
                description="Analyze log patterns and trends",
                handler=self._analyze_logs
            ),
            MenuItem(
                key="errors",
                label="Error Trends",
                description="View error trends and patterns",
                handler=self._view_error_trends
            ),
            MenuItem(
                key="export",
                label="Export Logs",
                description="Export logs to JSON or CSV format",
                handler=self._export_logs
            ),
            MenuItem(
                key="rotate",
                label="Rotate Logs",
                description="Force log rotation",
                handler=self._rotate_logs
            )
        ]

    def _configure_log_level(self) -> None:
        """Configure the logging level."""
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        self.ui.print_header("Configure Log Level", "Set the logging level")

        for i, level in enumerate(levels, 1):
            self.ui.print_info(f"{i}. {level}")

        choice = self.ui.get_input(
            "Select log level",
            [str(i) for i in range(1, len(levels) + 1)]
        )

        try:
            level = levels[int(choice) - 1]
            self.logging_manager.set_log_level(level)
            self.ui.print_success(f"Log level set to {level}")
        except Exception as e:
            self.ui.print_error(f"Failed to set log level: {str(e)}")

    def _view_recent_logs(self) -> None:
        """View recent log entries."""
        self.ui.print_header("Recent Logs", "View recent log entries")

        try:
            logs = self.logging_manager.get_recent_logs(n=50)
            for log in logs:
                if " - ERROR - " in log:
                    self.ui.print_error(log)
                elif " - WARNING - " in log:
                    self.ui.print_warning(log)
                else:
                    self.ui.print_info(log)
        except Exception as e:
            self.ui.print_error(f"Failed to retrieve logs: {str(e)}")

    def _analyze_logs(self) -> None:
        """Analyze log patterns and trends."""
        self.ui.print_header("Log Analysis", "Analyze log patterns")

        timeframes = ["24h", "7d", "30d"]
        for i, tf in enumerate(timeframes, 1):
            self.ui.print_info(f"{i}. Last {tf}")

        choice = self.ui.get_input(
            "Select timeframe",
            [str(i) for i in range(1, len(timeframes) + 1)]
        )

        try:
            timeframe = timeframes[int(choice) - 1]
            analysis = self.logging_manager.analyze_logs(timeframe)

            self.ui.print_info(f"\nLog Analysis for last {timeframe}:")
            self.ui.print_info(f"Total Entries: {analysis['total_entries']}")
            self.ui.print_error(f"Errors: {analysis['error_count']}")
            self.ui.print_warning(f"Warnings: {analysis['warning_count']}")
            self.ui.print_info(f"Info: {analysis['info_count']}")
            self.ui.print_info(f"Debug: {analysis['debug_count']}")

            if analysis['most_frequent_errors']:
                self.ui.print_info("\nMost Frequent Errors:")
                for error, count in analysis['most_frequent_errors'].items():
                    self.ui.print_error(f"{error}: {count} occurrences")
        except Exception as e:
            self.ui.print_error(f"Failed to analyze logs: {str(e)}")

    def _view_error_trends(self) -> None:
        """View error trends."""
        self.ui.print_header("Error Trends", "View error patterns")

        try:
            trends = self.logging_manager.get_error_trends(days=7)

            if not trends:
                self.ui.print_info("No errors found in the last 7 days")
                return

            self.ui.print_info("\nError trends for the last 7 days:")
            for error_type, count in trends.items():
                self.ui.print_error(f"{error_type}: {count} occurrences")
        except Exception as e:
            self.ui.print_error(f"Failed to retrieve error trends: {str(e)}")

    def _export_logs(self) -> None:
        """Export logs to a file."""
        self.ui.print_header("Export Logs", "Export logs to file")

        formats = ["json", "csv"]
        for i, fmt in enumerate(formats, 1):
            self.ui.print_info(f"{i}. {fmt.upper()}")

        choice = self.ui.get_input(
            "Select export format",
            [str(i) for i in range(1, len(formats) + 1)]
        )

        try:
            format = formats[int(choice) - 1]
            output_file = f"logs/export.{format}"
            self.logging_manager.export_logs(output_file, format)
            self.ui.print_success(f"Logs exported to {output_file}")
        except Exception as e:
            self.ui.print_error(f"Failed to export logs: {str(e)}")

    def _rotate_logs(self) -> None:
        """Force log rotation."""
        self.ui.print_header("Rotate Logs", "Force log rotation")

        try:
            self.logging_manager.rotate_logs()
            self.ui.print_success("Logs rotated successfully")
        except Exception as e:
            self.ui.print_error(f"Failed to rotate logs: {str(e)}")
