"""
Real-Time System Monitor (RTSM) - Monitor Class

This file contains the main RealTimeSystemMonitor class that handles the
system monitoring functionality and UI rendering.
"""

import os
import sys
import curses
import time
import json
from datetime import datetime
from utils import format_bytes
from system_info import get_system_info
from resource_usage import get_resource_usage
from ascii_art import get_ascii_art, ASCII_ART


class RealTimeSystemMonitor:
    """Main system monitor class"""
    
    def __init__(self, refresh_rate=1.0, custom_ascii=None, config_file=None, gpu_available=False):
        """Initialize the system monitor"""
        self.refresh_rate = refresh_rate
        self.custom_ascii = custom_ascii
        self.running = True
        self.gpu_available = gpu_available
        self.config = self.load_config(config_file)
        
    def load_config(self, config_file):
        """Load configuration from file or use defaults"""
        default_config = {
            "show_system_info": True,
            "show_ascii": True,
            "show_resources": True,
            "show_clock": True,
            "colors": {
                "title": curses.COLOR_CYAN,
                "label": curses.COLOR_GREEN,
                "value": curses.COLOR_WHITE,
                "ascii": curses.COLOR_YELLOW,
                "bar_filled": curses.COLOR_GREEN,
                "bar_empty": curses.COLOR_WHITE,
            }
        }
        
        if config_file:
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    # Merge user config with default
                    for key, value in user_config.items():
                        if isinstance(value, dict) and key in default_config:
                            default_config[key].update(value)
                        else:
                            default_config[key] = value
            except (FileNotFoundError, json.JSONDecodeError):
                pass
                
        return default_config
    
    def save_config(self, config_file):
        """Save configuration to file"""
        if config_file:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
    
    def draw_progress_bar(self, stdscr, y, x, width, percentage, filled_color, empty_color):
        """Draw a progress bar with color"""
        filled_width = int(width * percentage / 100)
        
        # Set colors for filled part
        stdscr.attron(curses.color_pair(filled_color))
        stdscr.addstr(y, x, "█" * filled_width)
        stdscr.attroff(curses.color_pair(filled_color))
        
        # Set colors for empty part
        stdscr.attron(curses.color_pair(empty_color))
        stdscr.addstr(y, x + filled_width, "░" * (width - filled_width))
        stdscr.attroff(curses.color_pair(empty_color))
    
    def curses_main(self, stdscr):
        """Main curses interface handler"""
        # Setup curses
        curses.curs_set(0)  # Hide cursor
        curses.start_color()
        curses.use_default_colors()
        
        # Initialize color pairs
        colors = self.config["colors"]
        curses.init_pair(1, colors["title"], -1)
        curses.init_pair(2, colors["label"], -1)
        curses.init_pair(3, colors["value"], -1)
        curses.init_pair(4, colors["ascii"], -1)
        curses.init_pair(5, colors["bar_filled"], -1)
        curses.init_pair(6, colors["bar_empty"], -1)
        
        # Main loop
        while self.running:
            try:
                # Clear screen
                stdscr.clear()
            except curses.error:
                # Handle curses errors (e.g., terminal resize)
                continue
                
                # Calculate dimensions and positions
                screen_height, screen_width = stdscr.getmaxyx()
                ascii_art = get_ascii_art(self.custom_ascii).splitlines()
                ascii_height = len(ascii_art)
                ascii_width = max(len(line) for line in ascii_art) if ascii_art else 0
                
                # Display ASCII art if enabled
                if self.config["show_ascii"]:
                    stdscr.attron(curses.color_pair(4))
                    for i, line in enumerate(ascii_art):
                        if i < screen_height:
                            stdscr.addstr(i, 0, line[:screen_width-1])
                    stdscr.attroff(curses.color_pair(4))
                
                # Display title
                title = "Real-Time System Monitor (RTSM)"
                stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(0, max(0, (screen_width - len(title)) // 2), title[:screen_width-1])
                stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
                
                # Starting position for system info
                info_x = ascii_width + 2
                info_y = 2
                
                # Display system information if enabled
                if self.config["show_system_info"]:
                    system_info = get_