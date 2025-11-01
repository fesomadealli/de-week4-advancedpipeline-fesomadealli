

import pandas as pd
import requests
from requests.exceptions import RequestException
from logger.logger import get_logger

class APIClient:
    """Handle all API communication."""

    def __init__(self, base_url: str, pagination_limit: int = 10):
        self.logger = get_logger("APIClient")
        self.BASE_URL = base_url
        self.LIMIT = pagination_limit
        self._product_cache = []
        self._user_cache = []

    def fetch_all_products(self, endpoint: str = '/products'):
        """Fetch all products once and store in cache."""
        url = self.BASE_URL + endpoint
        self.logger.info(f"Fetching products from {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            self._product_cache = response.json()
            self.logger.info(f"Fetched {len(self._product_cache)} products.")
        except RequestException as e:
            self._product_cache = []
            self.logger.error(f"Failed to fetch products: {e}")

    def get_all_users(self, endpoint: str = '/users'):
        """Fetch all users."""
        url = self.BASE_URL + endpoint
        self.logger.info(f"Fetching users from {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            self._user_cache = response.json()
            self.logger.info(f"Fetched {len(self._user_cache)} users.")
        except RequestException as e:
            self._user_cache = []
            self.logger.error(f"Failed to fetch users: {e}")

    def get_paginated_products(self):
        """Generator that yields products in chunks of `limit`."""
        self.logger.info("Paginating products...")
        for i in range(0, len(self._product_cache), self.LIMIT):
            chunk = self._product_cache[i:i + self.LIMIT]
            self.logger.debug(f"Yielding products {i} to {i + len(chunk)}")
            yield chunk

    def get_paginated_users(self):
        """Generator that yields users in chunks of `limit`."""
        self.logger.info("Paginating users...")
        for i in range(0, len(self._user_cache), self.LIMIT):
            chunk = self._user_cache[i:i + self.LIMIT]
            self.logger.debug(f"Yielding users {i} to {i + len(chunk)}")
            yield chunk