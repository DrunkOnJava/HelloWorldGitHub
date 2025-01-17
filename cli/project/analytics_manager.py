import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class AnalyticsManager:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.analytics_dir = os.path.join(project_root, '.analytics')
        self.ensure_analytics_directory()

    def ensure_analytics_directory(self) -> None:
        """Create analytics directory if it doesn't exist"""
        if not os.path.exists(self.analytics_dir):
            os.makedirs(self.analytics_dir)
            logger.info(f"Created analytics directory at {self.analytics_dir}")

    def track_feature_usage(self, feature_name: str, metadata: Optional[Dict] = None) -> None:
        """Track usage of a specific feature"""
        usage_file = os.path.join(self.analytics_dir, 'feature_usage.json')
        timestamp = datetime.now().isoformat()

        try:
            if os.path.exists(usage_file):
                with open(usage_file, 'r') as f:
                    usage_data = json.load(f)
            else:
                usage_data = {}

            if feature_name not in usage_data:
                usage_data[feature_name] = []

            usage_entry = {
                'timestamp': timestamp,
                'metadata': metadata or {}
            }

            usage_data[feature_name].append(usage_entry)

            with open(usage_file, 'w') as f:
                json.dump(usage_data, f, indent=2)

            logger.debug(f"Tracked usage of feature: {feature_name}")

        except Exception as e:
            logger.error(f"Failed to track feature usage: {str(e)}")

    def track_performance_metric(self, metric_name: str, value: float, context: Optional[Dict] = None) -> None:
        """Track a performance metric"""
        metrics_file = os.path.join(self.analytics_dir, 'performance_metrics.json')
        timestamp = datetime.now().isoformat()

        try:
            if os.path.exists(metrics_file):
                with open(metrics_file, 'r') as f:
                    metrics_data = json.load(f)
            else:
                metrics_data = {}

            if metric_name not in metrics_data:
                metrics_data[metric_name] = []

            metric_entry = {
                'timestamp': timestamp,
                'value': value,
                'context': context or {}
            }

            metrics_data[metric_name].append(metric_entry)

            with open(metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2)

            logger.debug(f"Tracked performance metric: {metric_name} = {value}")

        except Exception as e:
            logger.error(f"Failed to track performance metric: {str(e)}")

    def track_error(self, error_type: str, error_message: str, stack_trace: Optional[str] = None) -> None:
        """Track application errors"""
        errors_file = os.path.join(self.analytics_dir, 'error_tracking.json')
        timestamp = datetime.now().isoformat()

        try:
            if os.path.exists(errors_file):
                with open(errors_file, 'r') as f:
                    error_data = json.load(f)
            else:
                error_data = []

            error_entry = {
                'timestamp': timestamp,
                'type': error_type,
                'message': error_message,
                'stack_trace': stack_trace
            }

            error_data.append(error_entry)

            with open(errors_file, 'w') as f:
                json.dump(error_data, f, indent=2)

            logger.debug(f"Tracked error: {error_type} - {error_message}")

        except Exception as e:
            logger.error(f"Failed to track error: {str(e)}")

    def generate_usage_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
        """Generate a report of feature usage"""
        usage_file = os.path.join(self.analytics_dir, 'feature_usage.json')

        try:
            if not os.path.exists(usage_file):
                return {'features': {}, 'total_usage': 0}

            with open(usage_file, 'r') as f:
                usage_data = json.load(f)

            report = {'features': {}, 'total_usage': 0}

            for feature, usage_list in usage_data.items():
                filtered_usage = usage_list
                if start_date:
                    filtered_usage = [u for u in filtered_usage if u['timestamp'] >= start_date]
                if end_date:
                    filtered_usage = [u for u in filtered_usage if u['timestamp'] <= end_date]

                report['features'][feature] = len(filtered_usage)
                report['total_usage'] += len(filtered_usage)

            return report

        except Exception as e:
            logger.error(f"Failed to generate usage report: {str(e)}")
            return {'features': {}, 'total_usage': 0}

    def generate_performance_report(self, metric_name: Optional[str] = None) -> Dict:
        """Generate a report of performance metrics"""
        metrics_file = os.path.join(self.analytics_dir, 'performance_metrics.json')

        try:
            if not os.path.exists(metrics_file):
                return {'metrics': {}}

            with open(metrics_file, 'r') as f:
                metrics_data = json.load(f)

            report = {'metrics': {}}

            metrics_to_analyze = [metric_name] if metric_name else metrics_data.keys()

            for metric in metrics_to_analyze:
                if metric in metrics_data:
                    values = [entry['value'] for entry in metrics_data[metric]]
                    report['metrics'][metric] = {
                        'count': len(values),
                        'average': sum(values) / len(values) if values else 0,
                        'min': min(values) if values else 0,
                        'max': max(values) if values else 0
                    }

            return report

        except Exception as e:
            logger.error(f"Failed to generate performance report: {str(e)}")
            return {'metrics': {}}

    def analyze_error_trends(self) -> Dict:
        """Analyze error trends and patterns"""
        errors_file = os.path.join(self.analytics_dir, 'error_tracking.json')

        try:
            if not os.path.exists(errors_file):
                return {'error_types': {}, 'total_errors': 0}

            with open(errors_file, 'r') as f:
                error_data = json.load(f)

            error_types = {}
            for error in error_data:
                error_type = error['type']
                if error_type not in error_types:
                    error_types[error_type] = 0
                error_types[error_type] += 1

            return {
                'error_types': error_types,
                'total_errors': len(error_data)
            }

        except Exception as e:
            logger.error(f"Failed to analyze error trends: {str(e)}")
            return {'error_types': {}, 'total_errors': 0}

    def export_analytics_data(self, output_dir: str) -> bool:
        """Export all analytics data to a specified directory"""
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Export all analytics files
            for filename in os.listdir(self.analytics_dir):
                if filename.endswith('.json'):
                    src_path = os.path.join(self.analytics_dir, filename)
                    dst_path = os.path.join(output_dir, filename)

                    with open(src_path, 'r') as src, open(dst_path, 'w') as dst:
                        data = json.load(src)
                        json.dump(data, dst, indent=2)

            logger.info(f"Successfully exported analytics data to {output_dir}")
            return True

        except Exception as e:
            logger.error(f"Failed to export analytics data: {str(e)}")
            return False
