"""Logging and monitoring manager implementation."""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Dict, List, Optional
import json

class LoggingManager:
    """Manages logging and monitoring functionality."""

    def __init__(self, project_root: str):
        """Initialize logging manager.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.logs_dir = os.path.join(project_root, "logs")
        self.combined_log = os.path.join(self.logs_dir, "combined.log")
        self.error_log = os.path.join(self.logs_dir, "error.log")

        # Ensure logs directory exists
        os.makedirs(self.logs_dir, exist_ok=True)

        # Initialize logging configuration
        self._setup_logging()

        # Track error trends
        self.error_trends: Dict[str, int] = {}

    def _setup_logging(self) -> None:
        """Configure logging with rotation and different levels."""
        # Reset logging config
        logging.getLogger().handlers = []

        # Configure root logger
        logging.getLogger().setLevel(logging.DEBUG)

        # Combined log handler (all levels)
        combined_handler = logging.handlers.RotatingFileHandler(
            self.combined_log,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        combined_handler.setLevel(logging.DEBUG)
        combined_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        combined_handler.setFormatter(combined_formatter)
        logging.getLogger().addHandler(combined_handler)

        # Error log handler (ERROR and above)
        error_handler = logging.handlers.RotatingFileHandler(
            self.error_log,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        logging.getLogger().addHandler(error_handler)

    def set_log_level(self, level: str) -> None:
        """Set the logging level.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f'Invalid log level: {level}')
        logging.getLogger().setLevel(numeric_level)

    def get_recent_logs(self, n: int = 100, level: Optional[str] = None) -> List[str]:
        """Get the most recent log entries.

        Args:
            n: Number of log entries to retrieve
            level: Optional log level filter

        Returns:
            List of recent log entries
        """
        logs = []
        with open(self.combined_log, 'r') as f:
            for line in f.readlines()[-n:]:
                if level:
                    if f' - {level.upper()} - ' in line:
                        logs.append(line.strip())
                else:
                    logs.append(line.strip())
        return logs

    def get_error_trends(self, days: int = 7) -> Dict[str, int]:
        """Analyze error trends over time.

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary of error types and their frequencies
        """
        trends = {}
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)

        with open(self.error_log, 'r') as f:
            for line in f:
                try:
                    # Parse timestamp from log entry
                    timestamp_str = line.split(' - ')[0]
                    timestamp = datetime.strptime(
                        timestamp_str,
                        '%Y-%m-%d %H:%M:%S,%f'
                    ).timestamp()

                    if timestamp >= cutoff:
                        # Extract error type
                        error_type = line.split(' - ')[-1].split(':')[0].strip()
                        trends[error_type] = trends.get(error_type, 0) + 1
                except:
                    continue

        return trends

    def analyze_logs(self, timeframe: str = '24h') -> Dict:
        """Analyze logs for patterns and insights.

        Args:
            timeframe: Timeframe to analyze ('24h', '7d', '30d')

        Returns:
            Dictionary containing log analysis results
        """
        # Convert timeframe to seconds
        if timeframe.endswith('h'):
            seconds = int(timeframe[:-1]) * 3600
        elif timeframe.endswith('d'):
            seconds = int(timeframe[:-1]) * 86400
        else:
            raise ValueError(f'Invalid timeframe format: {timeframe}')

        cutoff = datetime.now().timestamp() - seconds

        analysis = {
            'total_entries': 0,
            'error_count': 0,
            'warning_count': 0,
            'info_count': 0,
            'debug_count': 0,
            'most_frequent_errors': {},
            'timeframe': timeframe
        }

        with open(self.combined_log, 'r') as f:
            for line in f:
                try:
                    # Parse timestamp
                    timestamp_str = line.split(' - ')[0]
                    timestamp = datetime.strptime(
                        timestamp_str,
                        '%Y-%m-%d %H:%M:%S,%f'
                    ).timestamp()

                    if timestamp >= cutoff:
                        analysis['total_entries'] += 1

                        # Count by level
                        if ' - ERROR - ' in line:
                            analysis['error_count'] += 1
                            error_msg = line.split(' - ERROR - ')[-1].strip()
                            analysis['most_frequent_errors'][error_msg] = \
                                analysis['most_frequent_errors'].get(error_msg, 0) + 1
                        elif ' - WARNING - ' in line:
                            analysis['warning_count'] += 1
                        elif ' - INFO - ' in line:
                            analysis['info_count'] += 1
                        elif ' - DEBUG - ' in line:
                            analysis['debug_count'] += 1
                except:
                    continue

        # Sort most frequent errors
        analysis['most_frequent_errors'] = dict(
            sorted(
                analysis['most_frequent_errors'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]  # Top 10 most frequent errors
        )

        return analysis

    def export_logs(self, output_file: str, format: str = 'json') -> None:
        """Export logs to a specific format.

        Args:
            output_file: Path to output file
            format: Export format ('json' or 'csv')
        """
        logs = []
        with open(self.combined_log, 'r') as f:
            for line in f:
                try:
                    # Parse log entry
                    parts = line.strip().split(' - ')
                    timestamp = parts[0]
                    name = parts[1]
                    level = parts[2]
                    message = ' - '.join(parts[3:])

                    logs.append({
                        'timestamp': timestamp,
                        'name': name,
                        'level': level,
                        'message': message
                    })
                except:
                    continue

        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(logs, f, indent=2)
        elif format == 'csv':
            import csv
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=['timestamp', 'name', 'level', 'message']
                )
                writer.writeheader()
                writer.writerows(logs)
        else:
            raise ValueError(f'Unsupported export format: {format}')

    def rotate_logs(self) -> None:
        """Force log rotation."""
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.doRollover()
