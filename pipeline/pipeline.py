


import json
from pipeline.config import ConfigManager
from pipeline.api_client import APIClient
from pipeline.data_enricher import DataEnricher
from pipeline.data_analyzer import DataAnalyzer
from logger.logger import get_logger

class Pipeline:
    """Orchestrates the full data pipeline from API to analysis."""

    def __init__(self, config_path='pipeline.cfg'):
        self.logger = get_logger("Pipeline", "pipeline.log")
        self.logger.info("Initializing pipeline...")
        self.config = ConfigManager(config_path)
        self.client = APIClient(
            base_url=self.config.base_url,
            pagination_limit=self.config.pagination_limit
        )

    def run(self):
        self.logger.info("🔧 Starting pipeline...")
        print("🔧 Starting pipeline...")

        # Step 1: Fetch products
        self.logger.info("📦 Fetching product data...")
        print("📦 Fetching product data...")
        self.client.fetch_all_products()
        all_products = self.client._product_cache.copy()

        for products_in_page in self.client.get_paginated_products():
            all_products.extend(products_in_page)
        self.logger.info(f"Total products collected: {len(all_products)}")

        # Step 2: Fetch users
        self.logger.info("👤 Fetching user data...")
        print("👤 Fetching user data...")
        self.client.get_all_users()
        all_users = self.client._user_cache.copy()

        for users_in_page in self.client.get_paginated_users():
            all_users.extend(users_in_page)
        self.logger.info(f"Total users collected: {len(all_users)}")

        # Step 3: Enrich data
        self.logger.info("🔗 Enriching data...")
        print("🔗 Enriching data...")
        enriched_df = DataEnricher.enrich_data(all_products, all_users)
        self.logger.info(f"Enriched data shape: {enriched_df.shape}")

        # Step 4: Analyze data
        self.logger.info("📊 Analyzing seller performance...")
        print("📊 Analyzing seller performance...")
        insights, tab_user_stats = DataAnalyzer.analyze(enriched_df, show_table=True)

        # Step 5: Save report
        self.logger.info("💾 Saving report to seller_performance_report.json...")
        print("💾 Saving report to seller_performance_report.json...")
        def convert_to_native(obj):
            if isinstance(obj, dict):
                return {k: convert_to_native(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native(v) for v in obj]
            elif hasattr(obj, "item"):
                return obj.item()
            else:
                return obj
        with open("seller_performance_report.json", "w", encoding="utf-8") as f:
            json.dump(convert_to_native(insights), f, indent=4)

        # with open("seller_performance_report.json", "w", encoding="utf-8") as f:
        #     json.dump(insights, f, indent=4)

        self.logger.info("📝 Saving summary to seller_performance_summary.txt...")
        print("📝 Saving summary to seller_performance_summary.txt...")
        with open("seller_performance_summary.txt", "w", encoding="utf-8") as f:
            f.write(tab_user_stats)

        self.logger.info("✅ Pipeline completed successfully.")
        print("✅ Pipeline completed successfully.")



        
