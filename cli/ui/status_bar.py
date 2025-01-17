"""Status bar for displaying system information and notifications."""

import queue
import threading
import time
from datetime import datetime

class StatusBar:
    """Status bar for displaying system information and notifications."""
    def __init__(self, ui):
        self.ui = ui
        self.message_queue = queue.Queue()
        self.current_status = ""
        self.start_time = datetime.now()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._update_loop, daemon=True)
        self._thread.start()

    def update(self, message: str, duration: int = 3) -> None:
        """Update status bar with a new message."""
        self.message_queue.put((message, duration))

    def _update_loop(self) -> None:
        """Background loop for status updates."""
        while not self._stop_event.is_set():
            try:
                message, duration = self.message_queue.get(timeout=0.1)
                self.current_status = message
                time.sleep(duration)
                self.current_status = ""
            except queue.Empty:
                continue

    def render(self) -> None:
        """Render the status bar."""
        width = self.ui.terminal_width
        uptime = datetime.now() - self.start_time
        uptime_str = f"Uptime: {str(uptime).split('.')[0]}"

        status = f" {self.current_status:<{width-len(uptime_str)-3}} {uptime_str} "
        print(f"{self.ui.theme.COLORS['SECONDARY']}{status}{self.ui.theme.COLORS['ENDC']}")

    def stop(self) -> None:
        """Stop the status bar update thread."""
        self._stop_event.set()
        self._thread.join()
