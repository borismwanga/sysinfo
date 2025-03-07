"""
Real-Time System Monitor (RTSM) - A Neofetch-like tool with live updates
"""

__version__ = "0.1.0"
__author__ = "RTSM Team"

# Check for required dependencies early
try:
    import psutil
except ImportError:
    raise ImportError(
        "Required package 'psutil' is not installed. "
        "Please install it using: pip install psutil"
    )

# Check for optional GPU monitoring
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

# Public API
from .monitor import RealTimeSystemMonitor
from .config import Config

__all__ = ["RealTimeSystemMonitor", "Config", "GPU_AVAILABLE"]