

import json
from pipeline.config import ConfigManager
from pipeline.api_client import APIClient
from pipeline.data_enricher import DataEnricher
from pipeline.data_analyzer import DataAnalyzer

class Pipeline:
    """Orchestrates the full data pipeline from API to analysis."""

    def __init__(self, config_path='pipeline.cfg'):  # C:\Users\HP\Downloads\codebook\omnicart_pipeline\pipeline.cfg
        self.config = ConfigManager(config_path)
        self.client = APIClient(
                                base_url=self.config.base_url,
                                pagination_limit=self.config.pagination_limit
                            )

    def run(self):
        print("🔧 Starting pipeline...")

        # Step 1: Fetch products
        print("📦 Fetching product data...")
        self.client.fetch_all_products()
        all_products = self.client._product_cache

        for products_in_page in self.client.get_paginated_products():
            all_products.extend(products_in_page)
        
        # Step 2: Fetch users
        print("👤 Fetching user data...")
        self.client.get_all_users()
        all_users = self.client._user_cache

        for users_in_page in self.client.get_paginated_users():
            all_users.extend(users_in_page)
        
        # Step 3: Enrich data
        print("🔗 Enriching data...")
        enriched_df = DataEnricher.enrich_data(all_products, all_users)

        # Step 4: Analyze data
        print("📊 Analyzing seller performance...")
        insights = DataAnalyzer.analyze(enriched_df, show_table=True) 

        # Step 5: Save report
        # print("💾 Saving report to seller_performance_report.json...")
        # with open("seller_performance_report.json", "w") as f:
        #     json.dump(insights, f, indent=4)

        print("✅ Pipeline completed successfully.")
