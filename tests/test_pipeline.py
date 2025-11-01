


import pytest
import requests_mock
import json
import os
from pipeline.pipeline import Pipeline
from logger.logger import get_logger

logger = get_logger("TestPipeline", "tests.log")

# Sample mock data
mock_products = [
    {"id": 1, "price": 100, "category": "electronics", "rating": {"rate": 4.5, "count": 10}},
    {"id": 2, "price": 200, "category": "jewelery", "rating": {"rate": 4.0, "count": 5}}
]

mock_users = [
    {"id": 1, "email": "a@example.com", "username": "user_a", "name": {"firstname": "A", "lastname": "Alpha"}, "address": {"city": "Lagos"}, "phone": "123"},
    {"id": 2, "email": "b@example.com", "username": "user_b", "name": {"firstname": "B", "lastname": "Beta"}, "address": {"city": "Abuja"}, "phone": "456"}
]

@pytest.fixture
def pipeline():
    return Pipeline(config_path='pipeline.cfg')

def test_pipeline_run_creates_reports(pipeline, requests_mock):
    # Mock endpoints
    requests_mock.get("https://fakestoreapi.com/products", json=mock_products)
    requests_mock.get("https://fakestoreapi.com/users", json=mock_users)

    # Run pipeline
    pipeline.run()

    # Check JSON report
    assert os.path.exists("seller_performance_report.json")
    with open("seller_performance_report.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        assert "user_a" in data
        assert "total_revenue" in data["user_a"]

    # Check TXT summary
    assert os.path.exists("seller_performance_summary.txt")
    with open("seller_performance_summary.txt", "r", encoding="utf-8") as f:
        content = f.read()
        assert "user_a" in content
        assert "Total Revenue" in content

    # Cleanup
    os.remove("seller_performance_report.json")
    os.remove("seller_performance_summary.txt")
    logger.info("✅ test_pipeline_run_creates_reports passed")
