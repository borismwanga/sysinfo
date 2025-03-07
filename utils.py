"""
Real-Time System Monitor (RTSM) - Utility Functions

This file contains utility functions used throughout the application.
"""

import os
import sys  # Add this import
import platform
import subprocess

def format_bytes(bytes_value):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.2f} PB"

def set_square_terminal_size(size=80):
    """
    Attempt to set the terminal to a square size (width x height)
    
    Args:
        size: The desired width and height in characters
        
    Returns:
        bool: True if successful, False otherwise
    """
    system = platform.system()
    
    try:
        if system == "Windows":
            # For Windows using PowerShell commands
            os.system(f'mode con: cols={size} lines={size}')
        elif system in ["Linux", "Darwin"]:  # Linux or macOS
            # Using stty and printf to resize terminal
            # First set rows and columns
            os.system(f'stty cols {size} rows {size}')
            
            # Then send an escape sequence to trigger resize in supported terminals
            sys.stdout.write(f"\x1b[8;{size};{size}t")
            sys.stdout.flush()
            
            # If xterm or similar terminal, try resize command
            try:
                subprocess.call(['resize', '-s', str(size), str(size)])
            except (subprocess.SubprocessError, FileNotFoundError):
                pass
        else:
            return False
        return True
    except Exception:
        return False