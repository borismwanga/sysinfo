#!/usr/bin/env python3
"""
Main entry point for the RTSM package
"""

import sys
import argparse
import time

from . import GPU_AVAILABLE
from .monitor import RealTimeSystemMonitor


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Real-Time System Monitor (RTSM)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-r", "--refresh", 
        type=float, 
        default=1.0,
        help="Refresh rate in seconds"
    )
    
    parser.add_argument(
        "-a", "--ascii", 
        type=str,
        help="Path to custom ASCII art file"
    )
    
    parser.add_argument(
        "-c", "--config", 
        type=str,
        help="Path to configuration file (JSON)"
    )
    
    parser.add_argument(
        "-v", "--version", 
        action="store_true",
        help="Show version information and exit"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the application"""
    args = parse_arguments()
    
    # Show version if requested
    if args.version:
        from . import __version__
        print(f"Real-Time System Monitor (RTSM) version {__version__}")
        return 0
    
    # Warn about optional modules
    if not GPU_AVAILABLE:
        print("Warning: 'GPUtil' module not found. GPU monitoring will be disabled.")
        print("To enable GPU monitoring, install GPUtil: pip install GPUtil")
        time.sleep(1.5)  # Give user time to read the warning
    
    try:
        # Run the monitor
        monitor = RealTimeSystemMonitor(
            refresh_rate=args.refresh,
            custom_ascii=args.ascii,
            config_file=args.config
        )
        monitor.run()
        return 0
    except KeyboardInterrupt:
        print("\nExiting RTSM...")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())