# config.py
"""
Handles configuration loading and saving.
"""
import json

def load_config(config_file):
    """Load configuration from file or return default settings."""
    default_config = {
        "show_system_info": True,
        "show_ascii": True,
        "show_resources": True,
        "show_clock": True,
        "colors": {
            "title": "cyan",
            "label": "green",
            "value": "white",
            "ascii": "yellow",
            "bar_filled": "green",
            "bar_empty": "white",
        }
    }
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_config

def save_config(config_file, config):
    """Save configuration to file."""
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)