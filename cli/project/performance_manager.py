"""Performance profiling and analysis functionality."""

import os
import time
import json
import psutil
from typing import List, Dict, Any, Optional
from PIL import Image
import glob
from pathlib import Path

class PerformanceManager:
    """Handles performance profiling and analysis."""
    def __init__(self, ui):
        self.ui = ui
        self.baseline_metrics = {}
        self.monitoring_active = False
        self.monitoring_interval = 5  # seconds
        self._load_baseline_metrics()

    def _load_baseline_metrics(self):
        """Load baseline performance metrics if they exist."""
        try:
            if os.path.exists('performance_baseline.json'):
                with open('performance_baseline.json', 'r') as f:
                    self.baseline_metrics = json.load(f)
        except Exception as e:
            self.ui.status_bar.update(f"Error loading baseline metrics: {str(e)}", 3)

    def run_cpu_profiling(self, duration: int) -> bool:
        """Run CPU profiling for specified duration."""
        try:
            # Use Node.js --prof flag for CPU profiling
            command = f"node --prof app.js & sleep {duration} && kill $!"
            return self.ui.run_command(command)
        except Exception as e:
            self.ui.status_bar.update(f"CPU profiling error: {str(e)}", 3)
            return False

    def run_memory_analysis(self) -> bool:
        """Run memory usage analysis."""
        try:
            # Use Node.js --heap-prof flag for heap profiling
            command = "node --heap-prof app.js"
            return self.ui.run_command(command)
        except Exception as e:
            self.ui.status_bar.update(f"Memory analysis error: {str(e)}", 3)
            return False

    def run_network_analysis(self, duration: int) -> bool:
        """Profile network requests."""
        try:
            # Use Chrome DevTools Protocol for network profiling
            command = f"lighthouse --only-categories=performance --output=json --output-path=./network-profile.json"
            return self.ui.run_command(command)
        except Exception as e:
            self.ui.status_bar.update(f"Network analysis error: {str(e)}", 3)
            return False

    def generate_flame_graph(self, duration: int) -> bool:
        """Generate CPU flame graph."""
        try:
            # Use 0x for generating flame graphs
            command = f"0x app.js -d {duration}"
            return self.ui.run_command(command)
        except Exception as e:
            self.ui.status_bar.update(f"Flame graph generation error: {str(e)}", 3)
            return False

    def track_web_vitals(self) -> bool:
        """Track Core Web Vitals metrics."""
        try:
            command = "lighthouse --only-categories=performance --output=json --output-path=./web-vitals.json"
            return self.ui.run_command(command)
        except Exception as e:
            self.ui.status_bar.update(f"Web Vitals tracking error: {str(e)}", 3)
            return False

    def start_real_time_monitoring(self) -> bool:
        """Start real-time performance monitoring."""
        try:
            self.monitoring_active = True
            while self.monitoring_active:
                metrics = {
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_usage': psutil.disk_usage('/').percent,
                    'network_io': psutil.net_io_counters()._asdict()
                }
                self.ui.status_bar.update(f"CPU: {metrics['cpu_percent']}% | RAM: {metrics['memory_percent']}%", 1)
                time.sleep(self.monitoring_interval)
            return True
        except Exception as e:
            self.ui.status_bar.update(f"Real-time monitoring error: {str(e)}", 3)
            return False

    def stop_real_time_monitoring(self):
        """Stop real-time performance monitoring."""
        self.monitoring_active = False

    def track_resource_usage(self, process_name: str) -> Dict[str, Any]:
        """Track resource usage for a specific process."""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                if process_name in proc.info['name']:
                    return {
                        'pid': proc.info['pid'],
                        'cpu_percent': proc.info['cpu_percent'],
                        'memory_percent': proc.info['memory_percent'],
                        'threads': proc.num_threads(),
                        'open_files': len(proc.open_files()),
                        'connections': len(proc.connections())
                    }
            return {}
        except Exception as e:
            self.ui.status_bar.update(f"Resource tracking error: {str(e)}", 3)
            return {}

    def detect_performance_regression(self, current_metrics: Dict[str, Any]) -> List[str]:
        """Detect performance regressions by comparing with baseline."""
        regressions = []
        threshold = 1.1  # 10% degradation threshold

        for metric, value in current_metrics.items():
            if metric in self.baseline_metrics:
                if value > self.baseline_metrics[metric] * threshold:
                    regressions.append(f"{metric} degraded by {((value/self.baseline_metrics[metric])-1)*100:.1f}%")

        return regressions

    def optimize_images(self, directory: str, quality: int = 85) -> bool:
        """Optimize images in the specified directory."""
        try:
            image_files = glob.glob(os.path.join(directory, "**/*.{jpg,jpeg,png}"), recursive=True)
            for img_path in image_files:
                with Image.open(img_path) as img:
                    # Convert RGBA to RGB if necessary
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    # Optimize and save
                    img.save(img_path, optimize=True, quality=quality)
            return True
        except Exception as e:
            self.ui.status_bar.update(f"Image optimization error: {str(e)}", 3)
            return False

    def analyze_code_splitting(self, build_stats_path: str) -> Dict[str, Any]:
        """Analyze webpack/rollup build stats for code splitting opportunities."""
        try:
            with open(build_stats_path, 'r') as f:
                stats = json.load(f)

            analysis = {
                'large_chunks': [],
                'duplicate_modules': [],
                'splitting_opportunities': []
            }

            # Analyze chunk sizes
            if 'chunks' in stats:
                for chunk in stats['chunks']:
                    if chunk['size'] > 244000:  # > 244KB
                        analysis['large_chunks'].append({
                            'name': chunk['names'][0],
                            'size': chunk['size']
                        })

            return analysis
        except Exception as e:
            self.ui.status_bar.update(f"Code splitting analysis error: {str(e)}", 3)
            return {}

    def suggest_lazy_loading(self, source_dir: str) -> List[str]:
        """Analyze code and suggest components for lazy loading."""
        suggestions = []
        try:
            react_files = glob.glob(os.path.join(source_dir, "**/*.{tsx,jsx}"), recursive=True)
            for file_path in react_files:
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Look for large component definitions
                    if len(content.split('\n')) > 200:  # Suggest lazy loading for large components
                        suggestions.append(f"Consider lazy loading {Path(file_path).stem} component")
            return suggestions
        except Exception as e:
            self.ui.status_bar.update(f"Lazy loading analysis error: {str(e)}", 3)
            return []
