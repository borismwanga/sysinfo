"""
Real-Time System Monitor (RTSM) - System Information Module

This file contains functions for retrieving system information
such as OS details, hostname, uptime, etc.
"""

import os
import platform
import socket
import shutil
import psutil
from datetime import datetime


def get_system_info():
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