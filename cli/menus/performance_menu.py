"""Performance tools menu interface."""

from typing import List
from cli.models.menu_item import MenuItem
from cli.project.performance_manager import PerformanceManager

class PerformanceMenu:
    """Menu interface for performance tools."""

    def __init__(self, ui, performance_manager: PerformanceManager = None):
        self.ui = ui
        self.performance_manager = performance_manager or PerformanceManager(ui)

    def get_menu_items(self) -> List[MenuItem]:
        """Get performance menu items."""
        return [
            MenuItem(
                "Real-time Monitoring",
                "Monitor system performance in real-time",
                self._handle_real_time_monitoring
            ),
            MenuItem(
                "Resource Usage",
                "Track resource usage for specific processes",
                self._handle_resource_tracking
            ),
            MenuItem(
                "Performance Regression",
                "Detect performance regressions",
                self._handle_regression_detection
            ),
            MenuItem(
                "Image Optimization",
                "Optimize images in the project",
                self._handle_image_optimization
            ),
            MenuItem(
                "Code Splitting Analysis",
                "Analyze and suggest code splitting opportunities",
                self._handle_code_splitting
            ),
            MenuItem(
                "Lazy Loading Suggestions",
                "Get suggestions for component lazy loading",
                self._handle_lazy_loading
            ),
            MenuItem(
                "CPU Profiling",
                "Run CPU profiling for performance analysis",
                self._handle_cpu_profiling
            ),
            MenuItem(
                "Memory Analysis",
                "Analyze memory usage and detect leaks",
                self._handle_memory_analysis
            ),
            MenuItem(
                "Network Analysis",
                "Profile network requests and performance",
                self._handle_network_analysis
            ),
            MenuItem(
                "Web Vitals",
                "Track Core Web Vitals metrics",
                self._handle_web_vitals
            )
        ]

    def _handle_real_time_monitoring(self) -> bool:
        """Handle real-time monitoring menu item."""
        try:
            self.ui.status_bar.update("Starting real-time monitoring (Ctrl+C to stop)...", 1)
            return self.performance_manager.start_real_time_monitoring()
        except KeyboardInterrupt:
            self.performance_manager.stop_real_time_monitoring()
            self.ui.status_bar.update("Monitoring stopped", 1)
            return True

    def _handle_resource_tracking(self) -> bool:
        """Handle resource tracking menu item."""
        process_name = self.ui.prompt("Enter process name to track: ")
        if not process_name:
            return False

        metrics = self.performance_manager.track_resource_usage(process_name)
        if metrics:
            self.ui.display_dict(metrics)
            return True
        return False

    def _handle_regression_detection(self) -> bool:
        """Handle performance regression detection menu item."""
        current_metrics = {
            'response_time': float(self.ui.prompt("Enter current response time (ms): ")),
            'memory_usage': float(self.ui.prompt("Enter current memory usage (MB): ")),
            'cpu_usage': float(self.ui.prompt("Enter current CPU usage (%): "))
        }

        regressions = self.performance_manager.detect_performance_regression(current_metrics)
        if regressions:
            self.ui.display_list("Performance Regressions Detected:", regressions)
        else:
            self.ui.status_bar.update("No performance regressions detected", 1)
        return True

    def _handle_image_optimization(self) -> bool:
        """Handle image optimization menu item."""
        directory = self.ui.prompt("Enter directory path to optimize images: ")
        if not directory:
            return False

        quality = self.ui.prompt("Enter image quality (1-100, default 85): ")
        quality = int(quality) if quality.isdigit() else 85

        return self.performance_manager.optimize_images(directory, quality)

    def _handle_code_splitting(self) -> bool:
        """Handle code splitting analysis menu item."""
        build_stats = self.ui.prompt("Enter path to build stats file: ")
        if not build_stats:
            return False

        analysis = self.performance_manager.analyze_code_splitting(build_stats)
        if analysis:
            self.ui.display_dict(analysis)
            return True
        return False

    def _handle_lazy_loading(self) -> bool:
        """Handle lazy loading suggestions menu item."""
        source_dir = self.ui.prompt("Enter source directory path: ")
        if not source_dir:
            return False

        suggestions = self.performance_manager.suggest_lazy_loading(source_dir)
        if suggestions:
            self.ui.display_list("Lazy Loading Suggestions:", suggestions)
            return True
        return False

    def _handle_cpu_profiling(self) -> bool:
        """Handle CPU profiling menu item."""
        duration = self.ui.prompt("Enter profiling duration in seconds: ")
        if not duration.isdigit():
            return False
        return self.performance_manager.run_cpu_profiling(int(duration))

    def _handle_memory_analysis(self) -> bool:
        """Handle memory analysis menu item."""
        return self.performance_manager.run_memory_analysis()

    def _handle_network_analysis(self) -> bool:
        """Handle network analysis menu item."""
        duration = self.ui.prompt("Enter analysis duration in seconds: ")
        if not duration.isdigit():
            return False
        return self.performance_manager.run_network_analysis(int(duration))

    def _handle_web_vitals(self) -> bool:
        """Handle Web Vitals tracking menu item."""
        return self.performance_manager.track_web_vitals()
