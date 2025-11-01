

import pytest
from pipeline.config import ConfigManager
from logger.logger import get_logger

logger = get_logger("TestConfig", "tests.log")

@pytest.fixture
def config():
    return ConfigManager('pipeline.cfg')

def test_base_url(config):
    assert config.base_url == 'https://fakestoreapi.com'

def test_config_values(config):
    assert config.base_url.startswith("https")
    assert isinstance(config.pagination_limit, int)
    logger.info("test_config_values passed")
