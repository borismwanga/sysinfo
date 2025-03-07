#!/usr/bin/env python3
"""
Real-Time System Monitor (RTSM) - A Neofetch-like tool with live updates

This standalone script runs the RTSM tool without requiring package installation.
"""

import os
import sys
import curses
import argparse
import time
import platform
import socket
import shutil
import json
from datetime import datetime
from pathlib import Path

# Add the current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Try to import required modules
try:
    import psutil
except ImportError:
    print("Error: Required module 'psutil' not found. Please install it using:")
    print("pip install psutil")
    sys.exit(1)

# Optional GPU monitoring
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False


# ASCII Art collection
ASCII_ART = {
    "linux": """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⢸⠉⠉⠉⠙⠺⣧⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⣼⣦⣬⡀⠀⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀
    ⠀⠀⢰⠿⠿⠿⣿⣿⣶⣦⣤⠾⢷⣾⣿⡆⠀⠀⠀
    ⠀⠀⢸⠀⠀⠀⣿⣿⣿⣿⡏⠀⠀⣿⣿⡇⠀⠀⠀
    ⠀⠀⠈⣦⣤⣤⡞⠛⠛⠏⠀⠰⣤⣼⠟⠀⠀⠀⠀
    ⠀⠀⠀⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """,
    "macos": """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡀⠀⠀
    ⠀⠀⠀⠀⠀⢀⣄⣴⣶⣶⣿⣿⣿⣿⣿⣿⡇⠀⠀
    ⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀
    ⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀
    ⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀
    ⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠈⠻⢿⣿⣿⣿⣿⡿⠏⠀⠀⠀⠀⠀⠀⠀
    """,
    "windows": """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⡠⠒⠁⠀⠀⠀⠀⠀⠈⠑⢄⠀⠀
    ⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣣⠀
    ⠀⠀⠀⠀⠀⠈⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠏⠀
    ⠀⠀⠀⠀⠀⠀⠈⠒⠤⣀⡀⠀⠀⠀⠀⢀⡌⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀
    """,
    "default": """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣶⣶⣿⣷⣆⠀⠀⠀⠀
    ⠀⠀⠀⢀⣤⣤⣶⣶⣾⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⡆⠀⠀⠀
    ⠀⢀⣴⣿⣿⣿⣿⣿⣿⡿⠛⠉⠉⠀⠀⠀⣿⣿⣿⣿⣷⠀⠀⠀
    ⢀⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣇⠀⠀
    ⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣆⠀
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⢻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⡟
    ⠀⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
    ⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀
    ⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀
    ⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀
    """
}


def format_bytes(bytes_value):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"


class RealTimeSystemMonitor:
    """Main system monitor class"""
    
    def __init__(self, refresh_rate=1.0, custom_ascii=None, config_file=None):
        """Initialize the system monitor"""
        self.refresh_rate = refresh_rate
        self.custom_ascii = custom_ascii
        self.running = True
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
    
    def get_ascii_art(self):
        """Get ASCII art for the current system or from custom file"""
        if self.custom_ascii:
            try:
                with open(self.custom_ascii, 'r') as f:
                    return f.read()
            except FileNotFoundError:
                pass
        
        # Default ASCII art based on OS
        system = platform.system().lower()
        if system in ASCII_ART:
            return ASCII_ART[system]
        return ASCII_ART["default"]  # Fallback
    
    def get_system_info(self):
        """Get system information"""
        info = {}
        
        # Basic system information
        info["OS"] = f"{platform.system()} {platform.release()}"
        info["Kernel"] = platform.version()
        info["Hostname"] = socket.gethostname()
        
        # Uptime
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        days, remainder = divmod(uptime.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        info["Uptime"] = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
        
        # Shell
        if platform.system() == "Windows":
            info["Shell"] = os.environ.get("COMSPEC", "cmd.exe")
        else:
            info["Shell"] = os.environ.get("SHELL", "/bin/sh")
        
        # Terminal size (as resolution)
        terminal_size = shutil.get_terminal_size()
        info["Terminal Size"] = f"{terminal_size.columns}x{terminal_size.lines}"
        
        # Desktop Environment
        if platform.system() == "Linux":
            info["Desktop"] = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
        elif platform.system() == "Darwin":
            info["Desktop"] = "Aqua"
        elif platform.system() == "Windows":
            info["Desktop"] = "Explorer"
        
        return info
    
    def get_resource_usage(self):
        """Get current resource usage"""
        resources = {}
        
        # CPU
        resources["CPU Usage"] = psutil.cpu_percent(interval=0.1)
        
        # Memory
        mem = psutil.virtual_memory()
        resources["Memory"] = {
            "total": mem.total,
            "used": mem.used,
            "percent": mem.percent
        }
        
        # GPU (if available)
        if GPU_AVAILABLE:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    resources["GPU"] = {
                        "name": gpus[0].name,
                        "usage": gpus[0].load * 100,
                        "memory": {
                            "total": gpus[0].memoryTotal,
                            "used": gpus[0].memoryUsed,
                            "percent": (gpus[0].memoryUsed / gpus[0].memoryTotal) * 100
                        }
                    }
            except Exception:
                pass
        
        return resources
    
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
                ascii_art = self.get_ascii_art().splitlines()
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
                    system_info = self.get_system_info()
                    
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
                    resources = self.get_resource_usage()
                    
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


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Real-Time System Monitor (RTSM)")
    parser.add_argument("-r", "--refresh", type=float, default=1.0,
                        help="Refresh rate in seconds (default: 1.0)")
    parser.add_argument("-a", "--ascii", type=str,
                        help="Path to custom ASCII art file")
    parser.add_argument("-c", "--config", type=str,
                        help="Path to configuration file (JSON)")
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Warn about optional modules
    if not GPU_AVAILABLE:
        print("Warning: 'GPUtil' module not found. GPU monitoring will be disabled.")
        print("To enable GPU monitoring, install GPUtil: pip install GPUtil")
        time.sleep(2)  # Give user time to read the warning
    
    # Run the monitor
    monitor = RealTimeSystemMonitor(
        refresh_rate=args.refresh,
        custom_ascii=args.ascii,
        config_file=args.config
    )
    monitor.run()


if __name__ == "__main__":
    main()