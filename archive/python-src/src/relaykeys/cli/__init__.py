"""
CLI tools for RelayKeys

This module provides command-line interface tools for:
- Sending keyboard and mouse commands
- Managing keymaps
- Running macros
"""

from .main import main as cli_main

__all__ = ["cli_main"]
