from scripts.processing import DataQualityEngine
from scripts.bigquery_loader import BigQueryLoader

engine = DataQualityEngine(
    "/opt/airflow/project/data/raw/customer_support_tickets.csv"
)

engine.process()

loader = BigQueryLoader()

loader.run(engine.clean_df)