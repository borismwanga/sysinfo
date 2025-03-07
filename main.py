#!/usr/bin/env python3
"""
Real-Time System Monitor (RTSM) - A Neofetch-like tool with live updates

This is the main entry point for the RTSM tool.
"""

import os
import sys
import argparse
import time
from monitor import RealTimeSystemMonitor
from utils import set_square_terminal_size

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


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Real-Time System Monitor (RTSM)")
    parser.add_argument("-r", "--refresh", type=float, default=1.0,
                       help="Refresh rate in seconds (default: 1.0)")
    parser.add_argument("-a", "--ascii", type=str,
                       help="Path to custom ASCII art file")
    parser.add_argument("-c", "--config", type=str,
                       help="Path to configuration file (JSON)")
    parser.add_argument("-s", "--square", type=int, 
                       help="Set terminal to square size (e.g. 80 for 80x80)")
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Set square terminal size if requested
    if args.square:
        if not set_square_terminal_size(args.square):
            print(f"Warning: Could not set terminal to {args.square}x{args.square}")
            print("The program will continue with the current terminal size.")
            time.sleep(2)  # Give user time to read the warning
    
    # Warn about optional modules
    if not GPU_AVAILABLE:
        print("Warning: 'GPUtil' module not found. GPU monitoring will be disabled.")
        print("To enable GPU monitoring, install GPUtil: pip install GPUtil")
        time.sleep(2)  # Give user time to read the warning
    
    # Run the monitor
    monitor = RealTimeSystemMonitor(
        refresh_rate=args.refresh,
        custom_ascii=args.ascii,
        config_file=args.config,
        gpu_available=GPU_AVAILABLE
    )
    monitor.run()


if __name__ == "__main__":
    main()