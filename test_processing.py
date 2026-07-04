from scripts.processing import DataQualityEngine

engine = DataQualityEngine(
    "data/raw/customer_support_tickets.csv"
)

engine.process()