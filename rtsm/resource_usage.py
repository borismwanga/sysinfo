"""
Resource usage monitoring for RTSM
"""

import psutil
from . import GPU_AVAILABLE

# Import GPU monitoring if available
if GPU_AVAILABLE:
    try:
        import GPUtil
    except ImportError:
        GPU_AVAILABLE = False


class ResourceMonitor:
    """Monitor system resource usage"""
    
    def __init__(self):
        """Initialize ResourceMonitor"""
        pass
    
    def get_resource_usage(self):
        """
        Get current resource usage
        
        Returns:
            dict: Resource usage information
        """
        resources = {}
        
        # CPU usage
        resources["CPU"] = self.get_cpu_usage()
        
        # Memory usage
        resources["Memory"] = self.get_memory_usage()
        
        # Disk usage
        resources["Disks"] = self.get_disk_usage()
        
        # GPU usage if available
        if GPU_AVAILABLE:
            gpu_info = self.get_gpu_usage()
            if gpu_info:
                resources["GPU"] = gpu_info
        
        return resources
    
    def get_cpu_usage(self):
        """
        Get CPU usage information
        
        Returns:
            dict: CPU usage information
        """
        cpu_info = {
            "percent": psutil.cpu_percent(interval=0.1),
            "per_core": psutil.cpu_percent(interval=0.1, percpu=True)
        }
        
        # Get load average on non-Windows systems
        if hasattr(psutil, "getloadavg"):
            try:
                load1, load5, load15 = psutil.getloadavg()
                cpu_info["load_avg"] = {
                    "1min": load1,
                    "5min": load5,
                    "15min": load15
                }
            except Exception:
                pass
        
        return cpu_info
    
    def get_memory_usage(self):
        """
        Get memory usage information
        
        Returns:
            dict: Memory usage information
        """
        # Virtual memory
        vm = psutil.virtual_memory()
        memory = {
            "total": vm.total,
            "available": vm.available,
            "used": vm.used,
            "free": vm.free,
            "percent": vm.percent
        }
        
        # Swap memory
        try:
            swap = psutil.swap_memory()
            memory["swap"] = {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent
            }
        except Exception:
            pass
        
        return memory
    
    def get_disk_usage(self):
        """
        Get disk usage information
        
        Returns:
            list: List of disk usage information dictionaries
        """
        disks = []
        
        # Get mountpoints and usage
        for partition in psutil.disk_partitions():
            if partition.fstype:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    })
                except (PermissionError, OSError):
                    # Skip if we can't access the disk
                    pass
        
        return disks
    
    def get_gpu_usage(self):
        """
        Get GPU usage information if available
        
        Returns:
            list: List of GPU information dictionaries or None if not available
        """
        if not GPU_AVAILABLE:
            return None
        
        try:
            gpus = GPUtil.getGPUs()
            if not gpus:
                return None
            
            gpu_info = []
            for gpu in gpus:
                gpu_info.append({
                    "id": gpu.id,
                    "name": gpu.name,
                    "load": gpu.load * 100,  # Convert to percentage
                    "memory": {
                        "total": gpu.memoryTotal,
                        "used": gpu.memoryUsed,
                        "free": gpu.memoryTotal - gpu.memoryUsed,
                        "percent": (gpu.memoryUsed / gpu.memoryTotal) * 100 if gpu.memoryTotal > 0 else 0
                    },
                    "temperature": gpu.temperature
                })
            return gpu_info
        except Exception:
            return None


# Allow direct execution for testing
if __name__ == "__main__":
    import json
    
    monitor = ResourceMonitor()
    resources = monitor.get_resource_usage()
    
    # Print formatted resource usage
    print("Resource Usage:")
    print(json.dumps(resources, indent=2, default=str))