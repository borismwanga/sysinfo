"""
Utility functions for RTSM
"""

def format_bytes(bytes_value):
    """
    Convert bytes to human-readable format
    
    Args:
        bytes_value (int): Size in bytes
        
    Returns:
        str: Human-readable size string
    """
    if bytes_value is None:
        return "N/A"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(bytes_value) < 1024:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024
    
    return f"{bytes_value:.2f} PB"


def format_percentage(value, decimals=1):
    """
    Format a percentage value
    
    Args:
        value (float): Percentage value
        decimals (int): Number of decimal places
        
    Returns:
        str: Formatted percentage string
    """
    if value is None:
        return "N/A"
    
    return f"{value:.{decimals}f}%"


def truncate_string(string, max_length=40):
    """
    Truncate a string to a maximum length
    
    Args:
        string (str): String to truncate
        max_length (int, optional): Maximum length. Defaults to 40.
        
    Returns:
        str: Truncated string
    """
    if not string:
        return ""
    
    if len(string) <= max_length:
        return string
    
    return string[:max_length-3] + "..."


def calculate_bar_width(percentage, width):
    """
    Calculate the width of a progress bar
    
    Args:
        percentage (float): Percentage value (0-100)
        width (int): Total width of the bar
        
    Returns:
        int: Width of the filled portion
    """
    if percentage is None:
        return 0
    
    # Ensure percentage is between 0 and 100
    percentage = max(0, min(100, percentage))
    
    # Calculate filled width
    return int(width * percentage / 100)


# Allow direct execution for testing
if __name__ == "__main__":
    # Test byte formatting
    sizes = [0, 100, 1024, 1024*1024, 1024*1024*1024, 1024*1024*1024*1024]
    for size in sizes:
        print(f"{size} bytes = {format_bytes(size)}")
    
    # Test percentage formatting
    percentages = [0, 12.34, 50, 99.99, 100]
    for pct in percentages:
        print(f"{pct} formatted = {format_percentage(pct)}")
    
    # Test string truncation
    strings = ["Short string", "This is a medium length string", "This is a very long string that should be truncated because it exceeds the maximum length"]
    for s in strings:
        print(f"Original: '{s}'")
        print(f"Truncated: '{truncate_string(s, 20)}'")
    
    # Test progress bar width calculation
    widths = [10, 20, 50, 100]
    percentages = [0, 25, 50, 75, 100]
    for w in widths:
        for p in percentages:
            filled = calculate_bar_width(p, w)
            empty = w - filled
            bar = f"[{'#' * filled}{' ' * empty}]"
            print(f"{p}% with width {w}: {bar}")