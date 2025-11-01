

import pandas as pd
from tabulate import tabulate
from logger.logger import get_logger

class DataAnalyzer:
    """Generate insights from enriched product-user data."""

    logger = get_logger("DataAnalyzer", "pipeline.log")

    @staticmethod
    def analyze(df: pd.DataFrame, show_table: bool = True) -> dict:
        pd.set_option('display.float_format', '{:,.2f}'.format)
        DataAnalyzer.logger.info("Starting seller performance analysis...")

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

            DataAnalyzer.logger.debug(
                f"{username}: ₦{total_revenue:,.2f} revenue, {product_count} products, "
                f"₦{avg_price:,.2f} avg price, {avg_rating:.2f} avg rating, "
                f"{total_quantity} quantity, top category: {top_category}"
            )

        tab_user_stats = ""
        if show_table:
            table = [
                [
                    user,
                    f"₦{data['total_revenue']:,.2f}",
                    data["products_sold"],
                    f"₦{data['average_price']:,.2f}",
                    f"{data['average_rating']:.2f}",
                    data["total_quantity"],
                    data["top_category"]
                ]
                for user, data in insights.items()
            ]
            headers = ["Username", "Total Revenue", "Products Sold", "Avg Price", "Avg Rating", "Total Quantity", "Top Category"]
            tab_user_stats = tabulate(table, headers=headers, tablefmt="grid")
            DataAnalyzer.logger.info("Seller performance table generated.")

        return insights, tab_user_stats
