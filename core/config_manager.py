"""
Configuration management module.

This module handles loading and saving application configuration.
"""

import json
import os
import logging

# Default configuration file
CONFIG_FILE = "finding_excellence_config.json"

class ConfigManager:
    """
    Manages application configuration.
    """
    
    def __init__(self, config_file=CONFIG_FILE):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """
        Load configuration from file.
        
        Returns:
            dict: Configuration data
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
        return {}
    
    def save_config(self):
        """
        Save current configuration to file.
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")
            return False
        return True
    
    def get(self, key, default=None):
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Value for the given key or default
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
            
        Returns:
            bool: True if successful
        """
        self.config[key] = value
        return True
    
    def update(self, new_values):
        """
        Update multiple configuration values.
        
        Args:
            new_values: Dictionary of new values
            
        Returns:
            bool: True if successful
        """
        self.config.update(new_values)
        return True
