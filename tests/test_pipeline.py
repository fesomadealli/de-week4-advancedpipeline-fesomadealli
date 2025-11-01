

import pytest
import requests_mock
import json
import os
from pipeline import Pipeline

# Sample mock data
mock_products = [
    {
        'id': 1,
        'price': 109.95,
        'category': "men's clothing",
        'rating': {'rate': 3.9, 'count': 120}
    },
    {
        'id': 2,
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
        'name': {'firstname': 'john', 'lastname': 'doe'}
    },
    {
        'id': 2,
        'email': 'morrison@gmail.com',
        'username': 'mor_2314',
        'name': {'firstname': 'david', 'lastname': 'morrison'}
    }
]

@pytest.fixture
def pipeline():
    return Pipeline(config_path='pipeline.cfg')

def test_pipeline_run_creates_report(pipeline, requests_mock):
    # Mock endpoints
    requests_mock.get('https://fakestoreapi.com/products', json=mock_products)
    requests_mock.get('https://fakestoreapi.com/users', json=mock_users)

    # Run pipeline
    pipeline.run()

    # Check output file
    assert os.path.exists("seller_performance_report.json")

    with open("seller_performance_report.json", "r") as f:
        data = json.load(f)

    # Validate structure
    assert isinstance(data, dict)
    assert "johnd" in data
    assert "mor_2314" in data
    assert "total_revenue" in data["johnd"]
    assert "products_sold" in data["mor_2314"]

    # Cleanup
    os.remove("seller_performance_report.json")
 