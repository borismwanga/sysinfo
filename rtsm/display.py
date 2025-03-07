"""
Display manager for RTSM using curses
"""

import curses
from datetime import datetime
from .utils import format_bytes, format_percentage, calculate_bar_width


class DisplayManager:
    """Manage the curses display"""
    
    def __init__(self, config):
        """
        Initialize the display manager
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.init_colors()
    
    def init_colors(self):
        """Initialize curses color pairs"""
        # Define color pairs
        self.COLOR_TITLE = 1
        self.COLOR_LABEL = 2
        self.COLOR_VALUE = 3
        self.COLOR_ASCII = 4
        self.COLOR_BAR_FILLED = 5
        self.COLOR_BAR_EMPTY = 6
        self.COLOR_WARNING = 7
        self.COLOR_CRITICAL = 8
        self.COLOR_GOOD = 9
        self.COLOR_INFO = 10
        
        # Set up colors if terminal supports it
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            
            # Get colors from config
            colors = self.config.get("colors", {})
            
            # Initialize color pairs
            curses.init_pair(self.COLOR_TITLE, colors.get("title", curses.COLOR_CYAN), -1)
            curses.init_pair(self.COLOR_LABEL, colors.get("label", curses.COLOR_GREEN), -1)
            curses.init_pair(self.COLOR_VALUE, colors.get("value", curses.COLOR_WHITE), -1)
            curses.init_pair(self.COLOR_ASCII, colors.get("ascii", curses.COLOR_YELLOW), -1)
            curses.init_pair(self.COLOR_BAR_FILLED, colors.get("bar_filled", curses.COLOR_GREEN), -1)
            curses.init_pair(self.COLOR_BAR_EMPTY, colors.get("bar_empty", curses.COLOR_WHITE), -1)
            curses.init_pair(self.COLOR_WARNING, curses.COLOR_YELLOW, -1)
            curses.init_pair(self.COLOR_CRITICAL, curses.COLOR_RED, -1)
            curses.init_pair(self.COLOR_GOOD, curses.COLOR_GREEN, -1)
            curses.init_pair(self.COLOR_INFO, curses.COLOR_BLUE, -1)
    
    def setup_screen(self, stdscr):
        """
        Set up the curses screen
        
        Args:
            stdscr: Curses standard screen
            
        Returns:
            stdscr: Configured screen
        """
        # Hide cursor
        curses.curs_set(0)
        
        # Enable keypad mode
        stdscr.keypad(True)
        
        # No delay for getch()
        stdscr.nodelay(True)
        
        return stdscr
    
    def draw_title(self, stdscr, title):
        """
        Draw the title centered at the top of the screen
        
        Args:
            stdscr: Curses screen
            title (str): Title text
        """
        screen_height, screen_width = stdscr.getmaxyx()
        
        # Draw title centered
        stdscr.attron(curses.color_pair(self.COLOR_TITLE) | curses.A_BOLD)
        title_x = max(0, (screen_width - len(title)) // 2)
        stdscr.addstr(0, title_x, title[:screen_width-1])
        stdscr.attroff(curses.color_pair(self.COLOR_TITLE) | curses.A_BOLD)
    
    def draw_ascii_art(self, stdscr, ascii_art):
        """
        Draw ASCII art on the screen
        
        Args:
            stdscr: Curses screen
            ascii_art (str): ASCII art string
            
        Returns:
            tuple: (height, width) of the ASCII art
        """
        if not self.config.get("show_ascii", True):
            return (0, 0)
            
        screen_height, screen_width = stdscr.getmaxyx()
        ascii_lines = ascii_art.splitlines()
        ascii_height = len(ascii_lines)
        ascii_width = max(len(line) for line in ascii_lines) if ascii_lines else 0
        
        # Draw the ASCII art
        stdscr.attron(curses.color_pair(self.COLOR_ASCII))
        for i, line in enumerate(ascii_lines):
            if i < screen_height - 1:  # Avoid bottom line
                start_x = 0
                stdscr.addstr(i + 2, start_x, line[:screen_width-1])
        stdscr.attroff(curses.color_pair(self.COLOR_ASCII))
        
        return (ascii_height, ascii_width)
    
    def draw_section_header(self, stdscr, y, x, title):
        """
        Draw a section header
        
        Args:
            stdscr: Curses screen
            y (int): Y position
            x (int): X position
            title (str): Section title
            
        Returns:
            int: New Y position after header
        """
        screen_height, screen_width = stdscr.getmaxyx()
        
        if y >= screen_height - 1:
            return y
        
        # Draw section header
        stdscr.attron(curses.color_pair(self.COLOR_LABEL) | curses.A_BOLD)
        stdscr.addstr(y, x, title[:screen_width - x - 1])
        stdscr.attroff(curses.color_pair(self.COLOR_LABEL) | curses.A_BOLD)
        
        return y + 1
    
    def draw_info_line(self, stdscr, y, x, label, value):
        """
        Draw a label: value information line
        
        Args:
            stdscr: Curses screen
            y (int): Y position
            x (int): X position
            label (str): Label text
            value (str): Value text
            
        Returns:
            int: New Y position after line
        """
        screen_height, screen_width = stdscr.getmaxyx()
        
        if y >= screen_height - 1:
            return y
        
        # Draw label
        stdscr.attron(curses.color_pair(self.COLOR_LABEL))
        stdscr.addstr(y, x, f"{label}: ")
        stdscr.attroff(curses.color_pair(self.COLOR_LABEL))
        
        # Calculate value position
        value_x = x + len(label) + 2
        max_value_width = screen_width - value_x - 1
        
        # Draw value
        if max_value_width > 0:
            stdscr.attron(curses.color_pair(self.COLOR_VALUE))
            stdscr.addstr(y, value_x, str(value)[:max_value_width])
            stdscr.attroff(curses.color_pair(self.COLOR_VALUE))
        
        return y + 1
    
    def draw_progress_bar(self, stdscr, y, x, width, percentage, label=None):
        """
        Draw a progress bar
        
        Args:
            stdscr: Curses screen
            y (int): Y position
            x (int): X position
            width (int): Width of the bar
            percentage (float): Percentage (0-100)
            label (str, optional): Label to show before percentage
            
        Returns:
            int: New Y position after bar
        """
        screen_height, screen_width = stdscr.getmaxyx()
        
        if y >= screen_height - 1:
            return y
        
        # Ensure reasonable width
        width = min(width, screen_width - x - 10)
        if width < 5:
            return y
        
        # Calculate filled width
        filled_width = calculate_bar_width(percentage, width)
        
        # Choose color based on percentage
        if percentage >= 90:
            fill_color = self.COLOR_CRITICAL
        elif percentage >= 70:
            fill_color = self.COLOR_WARNING
        else:
            fill_color = self.COLOR_BAR_FILLED
        
        # Draw label if provided
        if label:
            stdscr.attron(curses.color_pair(self.COLOR_LABEL))
            stdscr.addstr(y, x, f"{label}: ")
            stdscr.attroff(curses.color_pair(self.COLOR_LABEL))
            x += len(label) + 2
        
        # Draw percentage
        stdscr.attron(curses.color_pair(self.COLOR_VALUE))
        percent_str = f"{percentage:.1f}%"
        stdscr.addstr(y, x, percent_str)
        stdscr.attroff(curses.color_pair(self.COLOR_VALUE))
        
        # Draw progress bar
        bar_x = x + len(percent_str) + 1
        
        # Draw filled part
        stdscr.attron(curses.color_pair(fill_color))
        stdscr.addstr(y, bar_x, "█" * filled_width)
        stdscr.attroff(curses.color_pair(fill_color))
        
        # Draw empty part
        stdscr.attron(curses.color_pair(self.COLOR_BAR_EMPTY))
        stdscr.addstr(y, bar_x + filled_width, "░" * (width - filled_width))
        stdscr.attroff(curses.color_pair(self.COLOR_BAR_EMPTY))
        
        return y + 1
    
    def draw_system_info(self, stdscr, y, x, system_info):
        """
        Draw system information section
        
        Args:
            stdscr: Curses screen
            y (int): Y position
            x (int): X position
            system_info (dict): System information dictionary
            
        Returns:
            int: New Y position after section
        """
        if not self.config.get("show_system_info", True):
            return y
        
        # Draw section header
        y = self.draw_section_header(stdscr, y, x, "SYSTEM INFORMATION")
        
        # Draw each info line
        for key, value in system_info.items():
            y = self.draw_info_line(stdscr, y, x, key, value)
        
        return y + 1
    
    def draw_resource_usage(self, stdscr, y, x, resources):
        """
        Draw resource usage section
        
        Args:
            stdscr: Curses screen
            y (int): Y position
            x (int): X position
            resources (dict): Resource usage dictionary
            
        Returns:
            int: New Y position after section
        """
        if not self.config.get("show_resources", True):
            return y
        
        screen_height, screen_width = stdscr.getmaxyx()
        
        # Draw section header
        y = self.draw_section_header(stdscr, y, x, "RESOURCE USAGE")
        
        # CPU usage
        if "CPU" in resources:
            cpu = resources["CPU"]
            
            # Overall CPU usage
            cpu_percent = cpu["percent"]
            y = self.draw_progress_bar(stdscr, y, x, 40, cpu_percent, "CPU Usage")
            
            # Per-core usage if we have room
            if "per_core" in cpu and len(cpu["per_core"]) > 0 and y < screen_height - len(cpu["per_core"]) - 3:
                y = self.draw_info_line(stdscr, y, x, "CPU Cores", f"{len(cpu['per_core'])} cores")
                
                # Display each core's usage with a smaller bar
                for i, core_percent in enumerate(cpu["per_core"]):
                    if y < screen_height - 1:
                        core_label = f"Core {i}"
                        y = self.draw_progress_bar(stdscr, y, x + 2, 30, core_percent, core_label)
        
        # Memory usage
        if "Memory" in resources:
            mem = resources["Memory"]
            
            # Add a little spacing
            y += 1
            if y >= screen_height - 1:
                return y
            
            # Format values
            total_str = format_bytes(mem["total"])
            used_str = format_bytes(mem["used"])
            free_str = format_bytes(mem["available"])
            
            # Memory usage line and bar
            mem_line = f"Used: {used_str} / {total_str} (Free: {free_str})"
            y = self.draw_info_line(stdscr, y, x, "Memory", mem_line)
            y = self.draw_progress_bar(stdscr, y, x, 40, mem["percent"])
            
            # Swap usage if available
            if "swap" in mem and mem["swap"]["total"] > 0:
                # Add a little spacing
                y += 1
                if y >= screen_height - 1:
                    return y
                
                # Format swap values
                swap_total = format_bytes(mem["swap"]["total"])
                swap_used = format_bytes(mem["swap"]["used"])
                
                # Swap usage line and bar
                swap_line = f"Used: {swap_used} / {swap_total}"
                y = self.draw_info_line(stdscr, y, x, "Swap", swap_line)
                y = self.draw_progress_bar(stdscr, y, x, 40, mem["swap"]["percent"])
        
        # GPU usage
        if "GPU" in resources and resources["GPU"]:
            # Add a little spacing
            y += 1
            if y >= screen_height - 1:
                return y
            
            for gpu in resources["GPU"]:
                # GPU name
                gpu_name = f"{gpu['name']} (#{gpu['id']})"
                y = self.draw_info_line(stdscr, y, x, "GPU", gpu_name)
                
                # GPU usage bar
                y = self.draw_progress_bar(stdscr, y, x, 40, gpu["load"], "Load")
                
                # GPU memory
                mem = gpu["memory"]
                mem_total = f"{mem['total']:.0f} MB"
                mem_used = f"{mem['used']:.0f} MB"
                
                mem_line = f"Used: {mem_used} / {mem_total}"
                y = self.draw_info_line(stdscr, y, x, "GPU Memory", mem_line)
                y = self.draw_progress_bar(stdscr, y, x, 40, mem["percent"])
                
                # GPU temperature if available
                if "temperature" in gpu:
                    temp_str = f"{gpu['temperature']:.1f}°C"
                    y = self.draw_info_line(stdscr, y, x, "GPU Temp", temp_str)
        
        return y + 1
    
    def draw_clock(self, stdscr):
        """
        Draw clock at the bottom right of the screen
        
        Args:
            stdscr: Curses screen
        """
        if not self.config.get("show_clock", True):
            return
        
        screen_height, screen_width = stdscr.getmaxyx()
        
        # Get current time
        now = datetime.now()
        clock_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        # Draw clock at bottom right
        stdscr.attron(curses.color_pair(self.COLOR_TITLE) | curses.A_BOLD)
        clock_x = max(0, screen_width - len(clock_str) - 1)
        stdscr.addstr(screen_height - 2, clock_x, clock_str)
        stdscr.attroff(curses.color_pair(self.COLOR_TITLE) | curses.A_BOLD)
    
    def draw_help(self, stdscr):
        """
        Draw help text at the bottom of the screen
        
        Args:
            stdscr: Curses screen
        """
        screen_height, screen_width = stdscr.getmaxyx()
        
        # Help text
        help_text = "Press 'q' to quit, 's' to toggle sections, 'c' to configure, 'r' to refresh"
        
        # Draw help text at bottom
        stdscr.attron(curses.A_DIM)
        stdscr.addstr(screen_height - 1, 0, help_text[:screen_width-1])
        stdscr.attroff(curses.A_DIM)
    
    def render(self, stdscr, title, ascii_art, system_info, resources):
        """
        Render the entire display
        
        Args:
            stdscr: Curses screen
            title (str): Title text
            ascii_art (str): ASCII art string
            system_info (dict): System information dictionary
            resources (dict): Resource usage dictionary
        """
        # Clear screen
        stdscr.clear()
        
        # Setup screen (hide cursor, etc.)
        self.setup_screen(stdscr)
        
        # Draw title
        self.draw_title(stdscr, title)
        
        # Draw ASCII art
        ascii_height, ascii_width = self.draw_ascii_art(stdscr, ascii_art)
        
        # Calculate starting positions for info sections
        screen_height, screen_width = stdscr.getmaxyx()
        info_x = max(ascii_width + 2, screen_width // 3)
        info_y = 2  # Start below title
        
        # Draw system information
        info_y = self.draw_system_info(stdscr, info_y, info_x, system_info)
        
        # Draw resource usage
        info_y = self.draw_resource_usage(stdscr, info_y, info_x, resources)
        
        # Draw clock
        self.draw_clock(stdscr)
        
        # Draw help text
        self.draw_help(stdscr)
        
        # Refresh screen
        stdscr.refresh()