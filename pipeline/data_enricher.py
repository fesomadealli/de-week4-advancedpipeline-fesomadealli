

import pandas as pd

class DataEnricher:
    """Combines and cleans product and user data."""

    @staticmethod
    def enrich_data(products: list, users: list) -> pd.DataFrame:
        # Transform product data
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

        # Transform user data
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

        # Convert to DataFrames
        products_df = pd.DataFrame(product_records)
        users_df = pd.DataFrame(user_records)

        print("Products columns:", products_df.columns.tolist())
        print("Users columns:", users_df.columns.tolist())

        # Merge product and user data
        enriched_df = pd.merge(products_df, users_df, on="id", how="left")

        # Calculate revenue
        enriched_df["revenue"] = enriched_df["price"] * enriched_df["quantity"]

        # Drop Nulls
        enriched_df = enriched_df.dropna()

        return enriched_df
