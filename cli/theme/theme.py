"""Theme configuration for terminal UI."""

class Theme:
    """Theme configuration for terminal UI."""
    def __init__(self):
        self.COLORS = {
            'PRIMARY': '\033[38;5;75m',    # Bright Blue
            'SECONDARY': '\033[38;5;241m', # Gray
            'SUCCESS': '\033[38;5;78m',    # Green
            'WARNING': '\033[38;5;221m',   # Yellow
            'ERROR': '\033[38;5;196m',     # Red
            'INFO': '\033[38;5;147m',      # Purple
            'HEADER': '\033[38;5;51m',     # Cyan
            'ENDC': '\033[0m',
            'BOLD': '\033[1m',
            'DIM': '\033[2m',
            'ITALIC': '\033[3m',
            'UNDERLINE': '\033[4m',
        }

        self.SYMBOLS = {
            'arrow': '→',
            'bullet': '•',
            'check': '✓',
            'cross': '✗',
            'warning': '⚠',
            'info': 'ℹ',
            'star': '★',
            'box': '▢',
            'circle': '○',
            'diamond': '◇',
        }

        self.BORDERS = {
            'horizontal': '═',
            'vertical': '║',
            'top_left': '╔',
            'top_right': '╗',
            'bottom_left': '╚',
            'bottom_right': '╝',
            'separator': '─',
        }
