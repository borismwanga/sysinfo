"""
Real-Time System Monitor (RTSM) - ASCII Art Module

This file contains the ASCII art collection and related functions
for displaying system logos.
"""

import platform

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


def get_ascii_art(custom_ascii=None):
    """Get ASCII art for the current system or from custom file"""
    if custom_ascii:
        try:
            with open(custom_ascii, 'r') as f:
                return f.read()
        except FileNotFoundError:
            pass
    
    # Default ASCII art based on OS
    system = platform.system().lower()
    if system in ASCII_ART:
        return ASCII_ART[system]
    return ASCII_ART["default"]  # Fallback