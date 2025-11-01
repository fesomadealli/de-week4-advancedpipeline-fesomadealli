

import pandas as pd
from pipeline.data_enricher import DataEnricher
from logger.logger import get_logger

logger = get_logger("tests", "tests.log")

def test_enrich_data():
    products = [
        {"id": 1, "price": 100, "category": "electronics", "rating": {"rate": 4.5, "count": 10}},
        {"id": 2, "price": 200, "category": "jewelery", "rating": {"rate": 4.0, "count": 5}}
    ]
    users = [
        {"id": 1, "email": "a@example.com", "username": "user_a", "name": {"firstname": "A", "lastname": "Alpha"}, "address": {"city": "Lagos"}, "phone": "123"},
        {"id": 2, "email": "b@example.com", "username": "user_b", "name": {"firstname": "B", "lastname": "Beta"}, "address": {"city": "Abuja"}, "phone": "456"}
    ]
    df = DataEnricher.enrich_data(products, users)
    assert isinstance(df, pd.DataFrame)
    assert "revenue" in df.columns
    logger.info("test_enrich_data passed")
