"""Performance menu implementation."""

from ...models.menu_item import MenuItem

def show_performance_submenu(ui) -> None:
    """Performance profiling submenu."""
    while True:
        ui.print_header(
            "Performance Profiling",
            "Performance Analysis Tools"
        )

        menu_items = [
            MenuItem(
                key='cpu',
                label='CPU Profiling',
                description='Profile CPU usage',
                icon='💻',
                shortcut='c'
            ),
            MenuItem(
                key='memory',
                label='Memory Analysis',
                description='Analyze memory usage',
                icon='🧠',
                shortcut='m'
            ),
            MenuItem(
                key='network',
                label='Network Analysis',
                description='Profile network requests',
                icon='🌐',
                shortcut='n'
            ),
            MenuItem(
                key='flamegraph',
                label='Flame Graph',
                description='Generate flame graph',
                icon='🔥',
                shortcut='f'
            ),
            MenuItem(
                key='back',
                label='Back to Development Menu',
                icon='◀',
                shortcut='b'
            )
        ]

        ui.print_menu(menu_items)
        choice = ui.get_input("Select an option", menu_items)

        if choice == 'back':
            break
        elif choice == 'cpu':
            run_cpu_profiling(ui)
        elif choice == 'memory':
            run_memory_analysis(ui)
        elif choice == 'network':
            run_network_analysis(ui)
        elif choice == 'flamegraph':
            generate_flame_graph(ui)

def run_cpu_profiling(ui) -> None:
    """Run CPU profiling."""
    try:
        duration = int(ui.get_input("Profile duration (seconds)", required=True))
        if ui.project.run_cpu_profiling(duration):
            ui.status_bar.update("CPU profiling completed successfully", 3)
        else:
            ui.status_bar.update("CPU profiling failed", 3)
    except ValueError:
        ui.status_bar.update("Invalid duration", 3)

def run_memory_analysis(ui) -> None:
    """Run memory usage analysis."""
    if ui.project.run_memory_analysis():
        ui.status_bar.update("Memory analysis completed successfully", 3)
    else:
        ui.status_bar.update("Memory analysis failed", 3)

def run_network_analysis(ui) -> None:
    """Run network request profiling."""
    try:
        duration = int(ui.get_input("Profile duration (seconds)", required=True))
        if ui.project.run_network_analysis(duration):
            ui.status_bar.update("Network analysis completed successfully", 3)
        else:
            ui.status_bar.update("Network analysis failed", 3)
    except ValueError:
        ui.status_bar.update("Invalid duration", 3)

def generate_flame_graph(ui) -> None:
    """Generate CPU flame graph."""
    try:
        duration = int(ui.get_input("Profile duration (seconds)", required=True))
        if ui.project.generate_flame_graph(duration):
            ui.status_bar.update("Flame graph generated successfully", 3)
        else:
            ui.status_bar.update("Failed to generate flame graph", 3)
    except ValueError:
        ui.status_bar.update("Invalid duration", 3)
