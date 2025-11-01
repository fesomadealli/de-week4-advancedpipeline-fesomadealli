
Here’s your comprehensive and well-formatted `README.md`, Alli — tailored to your project brief, codebase, and testing strategy:

---

# 🛠️ OmniCart Analytics: Multi-Source Data Enrichment Pipeline

This project builds a robust ETL pipeline that fetches data from multiple API endpoints, handles pagination, enriches product data with seller information, and generates performance insights. Designed for real-world data engineering scenarios, it emphasizes modular design, configuration-driven execution, and testable components.

---

## 🎯 Learning Goals

- Design a robust API client that handles paginated responses
- Fetch and merge data from multiple endpoints using `pandas`
- Externalize pipeline settings via a configuration file
- Implement advanced data aggregation and analysis
- Write targeted unit tests for pagination, data joining, and configuration handling

---

## 🧩 Project Overview

You're a data engineer at **OmniCart Analytics**, tasked with building a pipeline that links product sales data to seller profiles. The data lives in two separate systems exposed via the [Fake Store API](https://fakestoreapi.com/):

- `/products`: Contains product details and sales metrics
- `/users`: Contains seller profiles

Your pipeline must:
- Handle large product datasets via pagination
- Enrich product records with seller metadata
- Analyze seller performance
- Output insights in both JSON and tabulated text formats

---

## ⚙️ Pipeline Architecture

### 1. `ConfigManager` (`config.py`)
- Loads settings from `pipeline.cfg`
- Provides access to:
  - `base_url`: API root
  - `pagination_limit`: chunk size for paginated fetches

### 2. `APIClient` (`api_client.py`)
- Fetches data from `/products` and `/users`
- Implements pagination using a generator pattern
- Handles network errors gracefully
- Caches responses for reuse

### 3. `DataEnricher` (`data_enricher.py`)
- Converts raw product and user lists into DataFrames
- Performs a left join on `id` to enrich product data with seller info
- Calculates `revenue = price × quantity`, where quantity is derived from `rating.count`
- Drops rows with nulls to ensure clean analysis

### 4. `DataAnalyzer` (`data_analyzer.py`)
- Groups enriched data by `username`
- Computes:
  - Total revenue
  - Number of products sold
  - Average price and rating
  - Total quantity sold
  - Most frequent product category
- Outputs:
  - A dictionary of seller metrics
  - A tabulated summary using `tabulate`

### 5. `Pipeline` (`pipeline.py`)
- Orchestrates the entire workflow:
  - Loads config
  - Fetches and paginates data
  - Enriches and analyzes
  - Saves results to:
    - `seller_performance_report.json`
    - `seller_performance_summary.txt`
- Logs all steps to `pipeline.log`

---

## 🔄 Pagination Strategy

The Fake Store API does not natively support pagination via query parameters. To simulate pagination:

- We fetch all products and users in one request
- Then yield chunks of data using a generator:
  ```python
  for i in range(0, len(data), limit):
      yield data[i:i + limit]
  ```
- This allows us to process large datasets in memory-efficient slices
- Pagination limit is configurable via `pipeline.cfg`

---

## 🧪 Testing Strategy

All tests are written using `pytest` and logged to `tests.log`.

### ✅ `test_api_client.py`
- Mocks API responses using `requests_mock`
- Verifies:
  - Product and user fetches
  - Pagination logic via generators

### ✅ `test_data_enricher.py`
- Tests:
  - Successful joins
  - Missing user edge cases
  - Revenue calculation
  - Null value dropping

### ✅ `test_data_analyzer.py`
- Validates:
  - Grouping by seller
  - Aggregation metrics
  - Tabulated output generation

### ✅ `test_config.py`
- Uses `tmp_path` to simulate config files
- Confirms correct parsing of settings

---

## 📁 Folder Structure

```
omnicart_pipeline/
├── pipeline/
│   ├── __init__.py
│   ├── config.py
│   ├── api_client.py
│   ├── data_enricher.py
│   ├── data_analyzer.py
│   └── pipeline.py
├── tests/
│   ├── __init__.py
│   ├── test_api_client.py
│   ├── test_config.py
│   ├── test_data_enricher.py
│   └── test_data_analyzer.py
├── main.py
├── pipeline.cfg
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Running the Pipeline

```bash
poetry install
poetry run python main.py
```

---

## 🧪 Running Tests with Coverage

```bash
poetry run pytest --cov=pipeline --cov-report=term-missing
```

To generate an HTML report:

```bash
poetry run pytest --cov=pipeline --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

---

## ✅ Submission Checklist

- [x] Repo name: `de-week4-advancedpipeline-<yourname>`
- [x] Branch: `feature/enrichment-pipeline`
- [x] Frequent commits with clear messages
- [x] README includes pagination and enrichment strategy
- [x] Pull Request opened to `main`

---

Absolutely, Alli! Here's the new section you can add to your `README.md` under the heading **"🚀 Running the Pipeline"** — formatted to match the rest of your document and tailored to your Poetry setup:

---

## 🚀 Running the Pipeline

To execute the full pipeline and generate seller performance insights:

### 1. Install Dependencies

If you're using Poetry:

```bash
poetry install
```

This installs all required packages listed in `pyproject.toml`.

---

### 2. Configure the Pipeline

Edit the `pipeline.cfg` file to set your API base URL and pagination limit:

```ini
[api]
base_url = https://fakestoreapi.com
pagination_limit = 5
```

---

### 3. Run the Pipeline

From the project root, run:

```bash
poetry run python main.py
```

This will:

- Fetch product and user data from the Fake Store API
- Enrich product data with seller information
- Analyze seller performance
- Save results to:
  - `seller_performance_report.json`
  - `seller_performance_summary.txt`

All execution logs will be saved to `pipeline.log`.

---
