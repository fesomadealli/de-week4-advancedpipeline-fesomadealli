

import pandas as pd
from pipeline.data_enricher import DataEnricher
from logger.logger import get_logger

logger = get_logger("TestEnricher", "tests.log")


def test_successful_enrichment():
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
    assert df.shape[0] == 2
    assert "revenue" in df.columns
    assert df["revenue"].iloc[0] == 1000
    logger.info("✅ test_successful_enrichment passed")


def test_missing_user_join():
    products = [
        {"id": 3, "price": 150, "category": "books", "rating": {"rate": 3.5, "count": 2}}
    ]
    users = [
        {"id": 1, "email": "a@example.com", "username": "user_a", "name": {"firstname": "A"}, "address": {"city": "Lagos"}, "phone": "123"}
    ]
    df = DataEnricher.enrich_data(products, users)
    # Should drop the unmatched row due to dropna()
    assert df.empty
    logger.info("✅ test_missing_user_join passed")


def test_revenue_calculation():
    products = [
        {"id": 1, "price": 50, "category": "toys", "rating": {"rate": 4.0, "count": 3}}
    ]
    users = [
        {"id": 1, "email": "c@example.com", "username": "user_c", "name": {"firstname": "C"}, "address": {"city": "Ibadan"}, "phone": "789"}
    ]
    df = DataEnricher.enrich_data(products, users)
    assert df["revenue"].iloc[0] == 150
    logger.info("✅ test_revenue_calculation passed")


def test_null_values_are_dropped():
    products = [
        {"id": 1, "price": None, "category": "electronics", "rating": {"rate": 4.5, "count": 10}},  # price is null
        {"id": 2, "price": 200, "category": "jewelery", "rating": {"rate": None, "count": 5}}      # rating is null
    ]
    users = [
        {"id": 1, "email": "a@example.com", "username": "user_a", "name": {"firstname": "A"}, "address": {"city": "Lagos"}, "phone": "123"},
        {"id": 2, "email": "b@example.com", "username": "user_b", "name": {"firstname": "B"}, "address": {"city": "Abuja"}, "phone": "456"}
    ]
    df = DataEnricher.enrich_data(products, users)

    # Both rows contain nulls in critical fields, so they should be dropped
    assert df.empty
    logger.info("✅ test_null_values_are_dropped passed")
