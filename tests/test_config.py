

import pytest
from pipeline.config import ConfigManager

@pytest.fixture
def config():
    return ConfigManager('pipeline.cfg')

def test_base_url(config):
    assert config.base_url == 'https://fakestoreapi.com'

def test_pagination_limit(config):
    assert config.pagination_limit == 10
