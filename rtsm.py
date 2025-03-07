#!/usr/bin/env python3
"""
Real-Time System Monitor (RTSM) - A Neofetch-like tool with live updates

This is a standalone script that can be run directly.
For the full package installation, use pip install rtsm
"""

import sys

# Try to import from the package if installed
try:
    from rtsm.__main__ import main
    
    if __name__ == "__main__":
        sys.exit(main())
        
# If not installed, run from the current directory
except ImportError:
    import os
    import inspect
    
    # Add the parent directory to sys.path
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    
    from rtsm.__main__ import main
    
    if __name__ == "__main__":
        sys.exit(main())