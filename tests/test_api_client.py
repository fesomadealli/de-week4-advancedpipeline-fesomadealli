

import pytest
import requests_mock
import requests
from pipeline.api_client import APIClient
from logger.logger import get_logger

logger = get_logger("TestAPIClient", "tests.log")

# Sample mock data
mock_products = [
    {
        'id': 1,
        'title': 'Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops',
        'price': 109.95,
        'category': "men's clothing",
        'rating': {'rate': 3.9, 'count': 120}
    },
    {
        'id': 2,
        'title': 'Mens Casual Premium Slim Fit T-Shirts',
        'price': 22.3,
        'category': "men's clothing",
        'rating': {'rate': 4.1, 'count': 259}
    }
]

mock_users = [
    {
        'id': 1,
        'email': 'john@gmail.com',
        'username': 'johnd',
        'name': {'firstname': 'john', 'lastname': 'doe'},
        'phone': '1-570-236-7033',
        'address': {'city': 'kilcoole'}
    },
    {
        'id': 2,
        'email': 'morrison@gmail.com',
        'username': 'mor_2314',
        'name': {'firstname': 'david', 'lastname': 'morrison'},
        'phone': '1-570-236-7033',
        'address': {'city': 'kilcoole'}
    }
]

@pytest.fixture
def client():
    return APIClient(base_url='https://fakestoreapi.com', pagination_limit=1)

def test_fetch_all_products(client, requests_mock):
    requests_mock.get('https://fakestoreapi.com/products', json=mock_products)
    client.fetch_all_products()
    assert client._product_cache == mock_products
    logger.info("✅ test_fetch_all_products passed")

def test_get_paginated_products(client, requests_mock):
    requests_mock.get('https://fakestoreapi.com/products', json=mock_products)
    client.fetch_all_products()

    pages = list(client.get_paginated_products())
    assert pages[0] == [mock_products[0]]
    assert pages[1] == [mock_products[1]]
    assert len(pages) == 2
    logger.info("✅ test_get_paginated_products passed")

def test_get_all_users(client, requests_mock):
    requests_mock.get('https://fakestoreapi.com/users', json=mock_users)
    client.get_all_users()
    assert client._user_cache == mock_users
    logger.info("✅ test_get_all_users passed")

def test_get_paginated_users(client, requests_mock):
    requests_mock.get('https://fakestoreapi.com/users', json=mock_users)
    client.get_all_users()

    pages = list(client.get_paginated_users())
    assert pages[0] == [mock_users[0]]
    assert pages[1] == [mock_users[1]]
    assert len(pages) == 2
    logger.info("✅ test_get_paginated_users passed")


def test_fetch_all_products_error(client, requests_mock):
    requests_mock.get('https://fakestoreapi.com/products', exc=requests.exceptions.RequestException("API down"))
    client.fetch_all_products()
    assert client._product_cache == []  # ensures fallback path executed


def test_get_all_users_error(client, requests_mock):
    requests_mock.get('https://fakestoreapi.com/users', exc=requests.exceptions.RequestException("API down"))
    client.get_all_users()
    assert client._user_cache == []  # ensures fallback path executed
