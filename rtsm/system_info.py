"""
System information collection for RTSM
"""

import os
import platform
import socket
import shutil
import psutil
from datetime import datetime


class SystemInfo:
    """Collect system information"""
    
    def __init__(self):
        """Initialize SystemInfo"""
        self.boot_time = datetime.fromtimestamp(psutil.boot_time())
    
    def get_system_info(self):
        """
        Get system information
        
        Returns:
            dict: System information dictionary
        """
        info = {}
        
        # Basic system information
        info["OS"] = f"{platform.system()} {platform.release()}"
        info["Kernel"] = platform.version()
        info["Hostname"] = socket.gethostname()
        
        # Uptime
        uptime = datetime.now() - self.boot_time
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
            
            # Try to get more detailed info on Linux
            try:
                # Distribution info
                import distro
                info["Distro"] = f"{distro.name()} {distro.version()}"
            except ImportError:
                pass
                
        elif platform.system() == "Darwin":
            info["Desktop"] = "Aqua"
            
            # macOS version
            mac_ver = platform.mac_ver()
            if mac_ver[0]:
                info["OS"] = f"macOS {mac_ver[0]}"
                
        elif platform.system() == "Windows":
            info["Desktop"] = "Explorer"
            
            # Windows version name
            win_ver = sys.getwindowsversion()
            if win_ver.major == 10:
                info["OS"] = "Windows 10"
            elif win_ver.major == 6 and win_ver.minor == 3:
                info["OS"] = "Windows 8.1"
            elif win_ver.major == 6 and win_ver.minor == 2:
                info["OS"] = "Windows 8"
            elif win_ver.major == 6 and win_ver.minor == 1:
                info["OS"] = "Windows 7"
        
        # CPU information
        cpu_info = self.get_cpu_info()
        info.update(cpu_info)
        
        return info
    
    def get_cpu_info(self):
        """
        Get CPU information
        
        Returns:
            dict: CPU information
        """
        info = {}
        
        try:
            # CPU name and cores
            info["CPU"] = platform.processor() or "Unknown CPU"
            info["CPU Cores"] = psutil.cpu_count(logical=False)
            info["CPU Threads"] = psutil.cpu_count(logical=True)
            
            # CPU frequency
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                if cpu_freq.current:
                    info["CPU Freq"] = f"{cpu_freq.current:.2f} MHz"
                if hasattr(cpu_freq, 'min') and hasattr(cpu_freq, 'max'):
                    if cpu_freq.min and cpu_freq.max:
                        info["CPU Range"] = f"{cpu_freq.min:.2f}-{cpu_freq.max:.2f} MHz"
        except Exception:
            # Some systems might not provide all CPU information
            pass
            
        return info


# Allow direct execution for testing
if __name__ == "__main__":
    import sys
    import json
    
    sys_info = SystemInfo()
    info = sys_info.get_system_info()
    
    # Print formatted information
    print("System Information:")
    print(json.dumps(info, indent=2))