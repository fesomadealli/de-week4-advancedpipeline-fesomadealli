


import pytest
import requests_mock
from pipeline.api_client import APIClient

# Sample mock data
mock_products = [
    {
        'id': 1,
        'title': 'Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops',
        'price': 109.95,
        'description': 'Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday',
        'category': "men's clothing",
        'image': 'https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_t.png',
        'rating': {'rate': 3.9, 'count': 120}
    },
    {
        'id': 2,
        'title': 'Mens Casual Premium Slim Fit T-Shirts ',
        'price': 22.3,
        'description': 'Slim-fitting style, contrast raglan long sleeve, three-button henley placket...',
        'category': "men's clothing",
        'image': 'https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_t.png',
        'rating': {'rate': 4.1, 'count': 259}
    }
]

mock_users = [
    {
        'id': 1,
        'email': 'john@gmail.com',
        'username': 'johnd',
        'password': 'm38rmF$',
        'name': {'firstname': 'john', 'lastname': 'doe'},
        'phone': '1-570-236-7033',
        'address': {
            'geolocation': {'lat': '-37.3159', 'long': '81.1496'},
            'city': 'kilcoole',
            'street': 'new road',
            'number': 7682,
            'zipcode': '12926-3874'
        },
        '__v': 0
    },
    {
        'id': 2,
        'email': 'morrison@gmail.com',
        'username': 'mor_2314',
        'password': '83r5^_',
        'name': {'firstname': 'david', 'lastname': 'morrison'},
        'phone': '1-570-236-7033',
        'address': {
            'geolocation': {'lat': '-37.3159', 'long': '81.1496'},
            'city': 'kilcoole',
            'street': 'Lovers Ln',
            'number': 7267,
            'zipcode': '12926-3874'
        },
        '__v': 0
    }
]

@pytest.fixture
def client():
    return APIClient(base_url='https://fakestoreapi.com', pagination_limit=1)

def test_fetch_all_products(client, requests_mock):
    requests_mock.get('https://fakestoreapi.com/products', json=mock_products)
    client.fetch_all_products()
    assert client._product_cache == mock_products

def test_get_next_product_page(client, requests_mock):
    requests_mock.get('https://fakestoreapi.com/products', json=mock_products)
    client.fetch_all_products()

    page1 = client.get_next_product_page()
    page2 = client.get_next_product_page()
    page3 = client.get_next_product_page()

    assert page1 == [mock_products[0]]
    assert page2 == [mock_products[1]]
    assert page3 == []

def test_get_all_users(client, requests_mock):
    requests_mock.get('https://fakestoreapi.com/users', json=mock_users)
    users = client.get_all_users()
    assert users == mock_users
