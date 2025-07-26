# Food Prices Kenya Project

This is a simple data platform for analyzing food prices in Kenya using batch processing with Airflow.

## Structure

- airflow/: Contains DAGs and scripts for data pipeline
- data/: Folders for raw, processed, and metadata
- sql/: SQL scripts for database setup
- dashboard/: Configuration for Grafana dashboard

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up Postgres database and run sql/create_tables.sql
3. Configure Airflow and set AIRFLOW_HOME if needed
4. Run the Airflow DAG: `airflow dags test price_pipeline`

Note: The get_data.py downloads the CSV automatically, but you can place your local wfp_food_prices_ken.csv in data/raw if preferred. 