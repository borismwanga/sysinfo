"""
Main monitor class for RTSM
"""

import os
import time
import curses
import platform

from .config import Config
from .system_info import SystemInfo
from .resource_usage import ResourceMonitor
from .display import DisplayManager
from .ascii_art import get_ascii_art


class RealTimeSystemMonitor:
    """Main monitor class for RTSM"""
    
    def __init__(self, refresh_rate=1.0, custom_ascii=None, config_file=None):
        """
        Initialize the system monitor
        
        Args:
            refresh_rate (float, optional): Refresh rate in seconds. Defaults to 1.0.
            custom_ascii (str, optional): Path to custom ASCII art file. Defaults to None.
            config_file (str, optional): Path to config file. Defaults to None.
        """
        # Initialize configuration
        self.config = Config(config_file)
        
        # Override refresh rate if specified
        if refresh_rate != 1.0:
            self.config.set("refresh_rate", refresh_rate)
        
        # Set up custom ASCII art path
        self.custom_ascii = custom_ascii
        
        # Initialize components
        self.system_info = SystemInfo()
        self.resource_monitor = ResourceMonitor()
        
        # Runtime state
        self.running = True
    
    def get_title(self):
        """
        Get the application title
        
        Returns:
            str: Application title
        """
        title = "Real-Time System Monitor (RTSM)"
        
        # Add version if available