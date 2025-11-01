
import configparser
import os

class ConfigManager:
    """ Reads the .cfg file and provides easy access to these settings. """
    
    def __init__(self, config_path='pipeline.cfg'):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
        
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    @property
    def base_url(self):
        return self.config.get('api', 'base_url')

    @property
    def pagination_limit(self):
        return self.config.getint('api', 'pagination_limit')


if __name__ == "__main__":
    config = ConfigManager()
    print("Base URL:", config.base_url)
    print("Pagination Limit:", config.pagination_limit)