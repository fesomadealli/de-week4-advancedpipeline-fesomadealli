
import pandas as pd
from logger.logger import get_logger

class DataEnricher:
    """Combines and cleans product and user data."""

    logger = get_logger("DataEnricher")

    @staticmethod
    def enrich_data(products: list, users: list) -> pd.DataFrame:
        DataEnricher.logger.info("Transforming product and user data...")

        product_records = [
            {
                "id": item.get("id"),
                "price": item.get("price"),
                "category": item.get("category"),
                "quantity": item.get("rating", {}).get("count", 0),
                "rating": item.get("rating", {}).get("rate", None)
            }
            for item in products
        ]

        user_records = [
            {
                "id": item.get("id"),
                "email": item.get("email"),
                "username": item.get("username"),
                "first_name": item.get("name", {}).get("firstname", ""),
                "last_name": item.get("name", {}).get("lastname", ""),
                "city": item.get("address", {}).get("city", ""),
                "phone": item.get("phone")
            }
            for item in users
        ]

        products_df = pd.DataFrame(product_records)
        users_df = pd.DataFrame(user_records)

        DataEnricher.logger.debug(f"Product columns: {products_df.columns.tolist()}")
        DataEnricher.logger.debug(f"User columns: {users_df.columns.tolist()}")

        enriched_df = pd.merge(products_df, users_df, on="id", how="left")
        enriched_df["revenue"] = enriched_df["price"] * enriched_df["quantity"]
        enriched_df = enriched_df.dropna()

        DataEnricher.logger.info(f"Enriched data shape: {enriched_df.shape}")
        return enriched_df
