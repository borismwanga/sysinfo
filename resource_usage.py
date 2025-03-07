"""
Real-Time System Monitor (RTSM) - Resource Usage Module

This file contains functions for retrieving system resource usage
such as CPU, memory, and GPU (if available).
"""

import psutil

# Conditionally import GPU monitoring capability
try:
    import GPUtil
except ImportError:
    pass


def get_resource_usage(gpu_available=False):
    """Get current resource usage"""
    resources = {}
    
    # CPU
    resources["CPU Usage"] = psutil.cpu_percent(interval=0.1)
    
    # Memory
    mem = psutil.virtual_memory()
    resources["Memory"] = {
        "total": mem.total,
        "used": mem.used,
        "percent": mem.percent
    }
    
    # GPU (if available)
    if gpu_available:
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                resources["GPU"] = {
                    "name": gpus[0].name,
                    "usage": gpus[0].load * 100,
                    "memory": {
                        "total": gpus[0].memoryTotal,
                        "used": gpus[0].memoryUsed,
                        "percent": (gpus[0].memoryUsed / gpus[0].memoryTotal) * 100
                    }
                }
        except Exception:
            pass
    
    return resources