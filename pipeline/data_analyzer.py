

import pandas as pd
from tabulate import tabulate

class DataAnalyzer:
    """Generate insights from enriched product-user data."""

    @staticmethod
    def analyze(df: pd.DataFrame, show_table: bool = True) -> dict:
        # Group by seller
        grouped = df.groupby("username")

        insights = {}

        for username, group in grouped:
            total_revenue = group["revenue"].sum()
            product_count = group.shape[0]
            avg_price = group["price"].mean()
            avg_rating = group["rating"].mean()
            total_quantity = group["quantity"].sum()
            top_category = group["category"].mode()[0] if not group["category"].mode().empty else None

            insights[username] = {
                "total_revenue": round(total_revenue, 2),
                "products_sold": product_count,
                "average_price": round(avg_price, 2),
                "average_rating": round(avg_rating, 2),
                "total_quantity": int(total_quantity),
                "top_category": top_category
            }

        if show_table:
            table = [
                [user,
                 data["total_revenue"],
                 data["products_sold"],
                 data["average_price"],
                 data["average_rating"],
                 data["total_quantity"],
                 data["top_category"]]
                for user, data in insights.items()
            ]
            headers = ["Username", "Total Revenue", "Products Sold", "Avg Price", "Avg Rating", "Total Quantity", "Top Category"]
            print(tabulate(table, headers=headers, tablefmt="grid"))

        return insights
