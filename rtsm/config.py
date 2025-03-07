"""
Configuration management for RTSM
"""

import os
import json
import curses
from pathlib import Path


class Config:
    """Configuration handler for RTSM"""
    
    # Default configuration
    DEFAULT_CONFIG = {
        "refresh_rate": 1.0,
        "show_system_info": True,
        "show_ascii": True,
        "show_resources": True,
        "show_clock": True,
        "colors": {
            "title": curses.COLOR_CYAN,
            "label": curses.COLOR_GREEN,
            "value": curses.COLOR_WHITE,
            "ascii": curses.COLOR_YELLOW,
            "bar_filled": curses.COLOR_GREEN,
            "bar_empty": curses.COLOR_WHITE,
        }
    }
    
    def __init__(self, config_file=None):
        """
        Initialize configuration
        
        Args:
            config_file (str, optional): Path to configuration file
        """
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """
        Load configuration from file or use defaults
        
        Returns:
            dict: Configuration dictionary
        """
        config = self.DEFAULT_CONFIG.copy()
        
        # Try to load config from file
        if self.config_file:
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    self._merge_configs(config, user_config)
            except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file: {e}")
                
        # Try to load from default locations if no config file specified
        elif not self.config_file:
            # Try user config dir
            user_config_dir = self._get_user_config_dir()
            default_config_path = os.path.join(user_config_dir, 'config.json')
            
            if os.path.exists(default_config_path):
                try:
                    with open(default_config_path, 'r') as f:
                        user_config = json.load(f)
                        self._merge_configs(config, user_config)
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Warning: Could not load default config file: {e}")
        
        return config
    
    def save_config(self, config_file=None):
        """
        Save configuration to file
        
        Args:
            config_file (str, optional): Path to configuration file
        """
        save_path = config_file or self.config_file
        
        # If no path specified, save to user config dir
        if not save_path:
            user_config_dir = self._get_user_config_dir()
            os.makedirs(user_config_dir, exist_ok=True)
            save_path = os.path.join(user_config_dir, 'config.json')
        
        try:
            with open(save_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuration saved to {save_path}")
        except IOError as e:
            print(f"Error saving configuration: {e}")
    
    def _merge_configs(self, base_config, user_config):
        """
        Recursively merge user config into base config
        
        Args:
            base_config (dict): Base configuration dictionary
            user_config (dict): User configuration dictionary
        """
        for key, value in user_config.items():
            if isinstance(value, dict) and key in base_config and isinstance(base_config[key], dict):
                self._merge_configs(base_config[key], value)
            else:
                base_config[key] = value
    
    def _get_user_config_dir(self):
        """
        Get user configuration directory
        
        Returns:
            str: Path to user config directory
        """
        # Use platform-specific config paths
        if os.name == 'posix':  # Linux/Mac
            config_dir = os.path.expanduser('~/.config/rtsm')
        else:  # Windows
            config_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'rtsm')
            
        return config_dir
    
    def get(self, key, default=None):
        """
        Get configuration value
        
        Args:
            key (str): Configuration key
            default: Default value if key not found
            
        Returns:
            The configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        Set configuration value
        
        Args:
            key (str): Configuration key
            value: Configuration value
        """
        self.config[key] = value
        
    def __getitem__(self, key):
        """Allow dictionary-like access to config"""
        return self.config[key]
    
    def __setitem__(self, key, value):
        """Allow dictionary-like setting of config values"""
        self.config[key] = value


# Allow direct execution for testing
if __name__ == "__main__":
    # Example usage
    config = Config()
    print("Default configuration:")
    print(json.dumps(config.config, indent=2))
    
    # Test setting and getting values
    config.set("refresh_rate", 0.5)
    print(f"Refresh rate: {config.get('refresh_rate')}")