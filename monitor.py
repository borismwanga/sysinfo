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
                    system_info = get_system_info()
                    
                    stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                    stdscr.addstr(info_y, info_x, "SYSTEM INFORMATION")
                    stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
                    info_y += 1
                    
                    for key, value in system_info.items():
                        if info_y < screen_height - 1:
                            stdscr.attron(curses.color_pair(2))
                            stdscr.addstr(info_y, info_x, f"{key}: ")
                            stdscr.attroff(curses.color_pair(2))
                            
                            stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(f"{value}"[:screen_width - info_x - len(key) - 3])
                            stdscr.attroff(curses.color_pair(3))
                            
                            info_y += 1
                
                # Display resource information if enabled
                if self.config["show_resources"]:
                    resources = get_resource_usage(self.gpu_available)
                    
                    info_y += 1
                    if info_y < screen_height - 1:
                        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                        stdscr.addstr(info_y, info_x, "RESOURCE USAGE")
                        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
                        info_y += 1
                    
                    # CPU
                    if info_y < screen_height - 1:
                        stdscr.attron(curses.color_pair(2))
                        stdscr.addstr(info_y, info_x, f"CPU Usage: ")
                        stdscr.attroff(curses.color_pair(2))
                        
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(f"{resources['CPU Usage']:.1f}%")
                        stdscr.attroff(curses.color_pair(3))
                        
                        # Draw progress bar
                        bar_width = min(40, screen_width - info_x - 20)
                        if bar_width > 5:
                            self.draw_progress_bar(
                                stdscr, info_y, info_x + 20, 
                                bar_width, resources['CPU Usage'],
                                5, 6
                            )
                        
                        info_y += 1
                    
                    # Memory
                    if info_y < screen_height - 1:
                        mem = resources["Memory"]
                        stdscr.attron(curses.color_pair(2))
                        stdscr.addstr(info_y, info_x, f"Memory: ")
                        stdscr.attroff(curses.color_pair(2))
                        
                        stdscr.attron(curses.color_pair(3))
                        mem_text = f"{format_bytes(mem['used'])} / {format_bytes(mem['total'])} ({mem['percent']:.1f}%)"
                        stdscr.addstr(mem_text[:screen_width - info_x - 8])
                        stdscr.attroff(curses.color_pair(3))
                        
                        info_y += 1
                        
                        # Draw memory progress bar
                        if info_y < screen_height - 1:
                            bar_width = min(40, screen_width - info_x - 10)
                            if bar_width > 5:
                                self.draw_progress_bar(
                                    stdscr, info_y, info_x + 10, 
                                    bar_width, mem['percent'],
                                    5, 6
                                )
                            info_y += 1
                    
                    # GPU (if available)
                    if "GPU" in resources and info_y < screen_height - 3:
                        gpu = resources["GPU"]
                        info_y += 1
                        
                        stdscr.attron(curses.color_pair(2))
                        stdscr.addstr(info_y, info_x, f"GPU: ")
                        stdscr.attroff(curses.color_pair(2))
                        
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(f"{gpu['name']}"[:screen_width - info_x - 6])
                        stdscr.attroff(curses.color_pair(3))
                        
                        info_y += 1
                        
                        if info_y < screen_height - 1:
                            stdscr.attron(curses.color_pair(2))
                            stdscr.addstr(info_y, info_x, f"GPU Usage: ")
                            stdscr.attroff(curses.color_pair(2))
                            
                            stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(f"{gpu['usage']:.1f}%")
                            stdscr.attroff(curses.color_pair(3))
                            
                            # Draw GPU usage progress bar
                            bar_width = min(40, screen_width - info_x - 20)
                            if bar_width > 5:
                                self.draw_progress_bar(
                                    stdscr, info_y, info_x + 20, 
                                    bar_width, gpu['usage'],
                                    5, 6
                                )
                            
                            info_y += 1
                        
                        if info_y < screen_height - 1:
                            stdscr.attron(curses.color_pair(2))
                            stdscr.addstr(info_y, info_x, f"GPU Memory: ")
                            stdscr.attroff(curses.color_pair(2))
                            
                            stdscr.attron(curses.color_pair(3))
                            vram_text = f"{gpu['memory']['used']:.1f} / {gpu['memory']['total']:.1f} MB ({gpu['memory']['percent']:.1f}%)"
                            stdscr.addstr(vram_text[:screen_width - info_x - 12])
                            stdscr.attroff(curses.color_pair(3))
                            
                            info_y += 1
                
                # Display clock if enabled
                if self.config["show_clock"]:
                    clock_y = screen_height - 2
                    now = datetime.now()
                    clock_str = now.strftime("%Y-%m-%d %H:%M:%S")
                    
                    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
                    stdscr.addstr(clock_y, max(0, screen_width - len(clock_str) - 1), clock_str)
                    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
                
                # Display help at the bottom
                help_text = "Press 'q' to quit, 'c' for config"
                stdscr.attron(curses.A_DIM)
                stdscr.addstr(screen_height - 1, 0, help_text[:screen_width-1])
                stdscr.attroff(curses.A_DIM)
                
                # Refresh the screen
                stdscr.refresh()
                
                # Handle input (non-blocking)
                stdscr.nodelay(True)
                key = stdscr.getch()
                
                if key == ord('q'):
                    self.running = False
                elif key == ord('c'):
                    # Toggle features
                    self.config["show_system_info"] = not self.config["show_system_info"]
                
                # Sleep for refresh rate
                time.sleep(self.refresh_rate)
                
            except KeyboardInterrupt:
                self.running = False
            except curses.error:
                # Terminal size might have changed, just continue
                pass
    
    def run(self):
        """Run the monitor"""
        curses.wrapper(self.curses_main)