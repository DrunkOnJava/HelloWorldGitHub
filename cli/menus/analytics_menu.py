import os
from datetime import datetime, timedelta
from typing import Optional
from ..models.menu_item import MenuItem
from ..project.analytics_manager import AnalyticsManager

class AnalyticsMenu:
    def __init__(self, project_root: str):
        self.analytics_manager = AnalyticsManager(project_root)

    def get_menu_items(self) -> list[MenuItem]:
        return [
            MenuItem(
                "Track Feature Usage",
                "Record usage of specific features",
                self.track_feature
            ),
            MenuItem(
                "Track Performance",
                "Record performance metrics",
                self.track_performance
            ),
            MenuItem(
                "Track Error",
                "Record application errors",
                self.track_error
            ),
            MenuItem(
                "Generate Usage Report",
                "Generate feature usage analytics report",
                self.generate_usage_report
            ),
            MenuItem(
                "Generate Performance Report",
                "Generate performance metrics report",
                self.generate_performance_report
            ),
            MenuItem(
                "Analyze Error Trends",
                "View error patterns and trends",
                self.analyze_errors
            ),
            MenuItem(
                "Export Analytics Data",
                "Export all analytics data",
                self.export_data
            )
        ]

    def track_feature(self) -> None:
        """Menu handler for tracking feature usage"""
        feature_name = input("Enter feature name: ")
        metadata = {}

        while True:
            key = input("Enter metadata key (or press enter to finish): ")
            if not key:
                break
            value = input(f"Enter value for {key}: ")
            metadata[key] = value

        self.analytics_manager.track_feature_usage(feature_name, metadata)
        print(f"Successfully tracked usage of feature: {feature_name}")

    def track_performance(self) -> None:
        """Menu handler for tracking performance metrics"""
        metric_name = input("Enter metric name: ")
        try:
            value = float(input("Enter metric value: "))
        except ValueError:
            print("Error: Metric value must be a number")
            return

        context = {}
        while True:
            key = input("Enter context key (or press enter to finish): ")
            if not key:
                break
            value = input(f"Enter value for {key}: ")
            context[key] = value

        self.analytics_manager.track_performance_metric(metric_name, value, context)
        print(f"Successfully tracked performance metric: {metric_name}")

    def track_error(self) -> None:
        """Menu handler for tracking errors"""
        error_type = input("Enter error type: ")
        error_message = input("Enter error message: ")
        stack_trace = input("Enter stack trace (optional): ")

        self.analytics_manager.track_error(
            error_type,
            error_message,
            stack_trace if stack_trace else None
        )
        print("Successfully tracked error")

    def generate_usage_report(self) -> None:
        """Menu handler for generating usage reports"""
        start_date = input("Enter start date (YYYY-MM-DD) or press enter for all time: ")
        end_date = input("Enter end date (YYYY-MM-DD) or press enter for current: ")

        report = self.analytics_manager.generate_usage_report(
            start_date if start_date else None,
            end_date if end_date else None
        )

        print("\nFeature Usage Report:")
        print("-" * 40)
        print(f"Total Usage: {report['total_usage']}")
        print("\nFeature Breakdown:")
        for feature, count in report['features'].items():
            print(f"- {feature}: {count} uses")

    def generate_performance_report(self) -> None:
        """Menu handler for generating performance reports"""
        metric_name = input("Enter metric name (or press enter for all metrics): ")

        report = self.analytics_manager.generate_performance_report(
            metric_name if metric_name else None
        )

        print("\nPerformance Metrics Report:")
        print("-" * 40)
        for metric, stats in report['metrics'].items():
            print(f"\nMetric: {metric}")
            print(f"Count: {stats['count']}")
            print(f"Average: {stats['average']:.2f}")
            print(f"Min: {stats['min']}")
            print(f"Max: {stats['max']}")

    def analyze_errors(self) -> None:
        """Menu handler for analyzing error trends"""
        trends = self.analytics_manager.analyze_error_trends()

        print("\nError Trends Analysis:")
        print("-" * 40)
        print(f"Total Errors: {trends['total_errors']}")
        print("\nError Types Breakdown:")
        for error_type, count in trends['error_types'].items():
            print(f"- {error_type}: {count} occurrences")

    def export_data(self) -> None:
        """Menu handler for exporting analytics data"""
        output_dir = input("Enter output directory path: ")

        if self.analytics_manager.export_analytics_data(output_dir):
            print(f"Successfully exported analytics data to {output_dir}")
        else:
            print("Failed to export analytics data")
