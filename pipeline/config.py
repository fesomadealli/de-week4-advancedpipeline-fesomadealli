

import configparser
import os
from logger.logger import get_logger

class ConfigManager:
    """Reads the .cfg file and provides easy access to these settings."""

    def __init__(self, config_path='pipeline.cfg'):
        self.logger = get_logger("ConfigManager")
        if not os.path.exists(config_path):
            self.logger.error(f"Configuration file '{config_path}' not found.")
            raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
        
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.logger.info(f"Loaded configuration from {config_path}")

    @property
    def base_url(self):
        url = self.config.get('api', 'base_url')
        self.logger.debug(f"Base URL: {url}")
        return url

    @property
    def pagination_limit(self):
        limit = self.config.getint('api', 'pagination_limit')
        self.logger.debug(f"Pagination Limit: {limit}")
        return limit
