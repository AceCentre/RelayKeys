"""
GUI components for RelayKeys

This module provides graphical user interface components:
- Qt-based main application
- System tray integration
- Configuration dialogs
"""

from .qt_app import main as gui_main

__all__ = ["gui_main"]
