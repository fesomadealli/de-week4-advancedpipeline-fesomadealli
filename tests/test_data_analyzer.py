

import pandas as pd
from pipeline.data_analyzer import DataAnalyzer
from logger.logger import get_logger

logger = get_logger("TestAnalyzer", "tests.log")

def test_analyze_returns_correct_metrics():
    data = {
        "username": ["user_a", "user_a", "user_b"],
        "price": [100, 200, 300],
        "rating": [4.5, 4.0, 5.0],
        "quantity": [10, 5, 2],
        "category": ["electronics", "electronics", "jewelery"],
        "revenue": [1000, 1000, 600]
    }
    df = pd.DataFrame(data)
    insights, table = DataAnalyzer.analyze(df, show_table=False)

    assert "user_a" in insights
    assert insights["user_a"]["total_revenue"] == 2000.00
    assert insights["user_a"]["products_sold"] == 2
    assert insights["user_a"]["average_price"] == 150.00
    assert insights["user_a"]["top_category"] == "electronics"

    assert "user_b" in insights
    assert insights["user_b"]["total_quantity"] == 2
    assert insights["user_b"]["average_rating"] == 5.00

    logger.info("✅ test_analyze_returns_correct_metrics passed")


# poetry run pytest tests/
# poetry run pytest --cov=pipeline tests/
