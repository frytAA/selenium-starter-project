"""
Configuration manager for test environment settings.
"""
import os
import json
from pathlib import Path


class ConfigManager:
    """
    Manages configuration settings for different test environments.
    
    Example config.json:
    {
        "default": {
            "base_url": "https://www.example.com",
            "timeout": 10,
            "screenshot_on_failure": true,
            "headless": false
        },
        "dev": {
            "base_url": "https://dev.example.com",
            "timeout": 15
        },
        "staging": {
            "base_url": "https://staging.example.com"
        },
        "prod": {
            "base_url": "https://www.example.com"
        }
    }
    """
    
    def __init__(self, config_file="config.json"):
        """
        Initialize the configuration manager.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.environment = os.environ.get("TEST_ENV", "default")
        
    def _load_config(self):
        """
        Load configuration from the config file.
        
        Returns:
            dict: Configuration settings
        """
        # Default configuration
        default_config = {
            "default": {
                "base_url": "https://www.google.com",
                "timeout": 10,
                "screenshot_on_failure": True,
                "headless": False,
                "browser": "chrome"
            }
        }
        
        # Load from file if it exists
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing config file: {e}")
                return default_config
        else:
            # Create a default config file
            self._create_default_config(default_config)
            return default_config
    
    def _create_default_config(self, config):
        """
        Create a default configuration file.
        
        Args:
            config (dict): Default configuration
        """
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=4)
            print(f"Created default configuration file: {self.config_file}")
        except Exception as e:
            print(f"Error creating default config file: {e}")
    
    def get(self, key, default=None):
        """
        Get a configuration value.
        
        Args:
            key (str): The configuration key
            default: Default value if key doesn't exist
            
        Returns:
            The configuration value
        """
        # Check environment variables first
        env_var = f"TEST_{key.upper()}"
        if env_var in os.environ:
            return os.environ[env_var]
        
        # Check environment-specific config
        if self.environment in self.config and key in self.config[self.environment]:
            return self.config[self.environment][key]
        
        # Check default config
        if "default" in self.config and key in self.config["default"]:
            return self.config["default"][key]
        
        # Return default value
        return default
    
    def set_environment(self, environment):
        """
        Set the current environment.
        
        Args:
            environment (str): The environment to use
        """
        self.environment = environment


# Create a singleton instance
config = ConfigManager()

# Example usage:
# from config_manager import config
# base_url = config.get("base_url")
# timeout = config.get("timeout", 10)