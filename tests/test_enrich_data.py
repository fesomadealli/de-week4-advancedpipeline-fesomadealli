

import pytest
from pipeline.data_enricher import DataEnricher

def test_enrich_data():
    products = [
        {"id": 1, "price": 100, "category": "tech", "rating": {"rate": 4.5, "count": 10}},
        {"id": 2, "price": 50, "category": "books", "rating": {"rate": 3.8, "count": 5}}
    ]
    users = [
        {"id": 1, "email": "a@example.com", "username": "userA", "name": {"firstname": "Alice", "lastname": "Smith"}},
        {"id": 2, "email": "b@example.com", "username": "userB", "name": {"firstname": "Bob", "lastname": "Jones"}}
    ]

    df = DataEnricher.enrich_data(products, users)
    assert df.shape[0] == 2
    assert "revenue" in df.columns
    assert df.loc[df["id"] == 1, "revenue"].values[0] == 1000
