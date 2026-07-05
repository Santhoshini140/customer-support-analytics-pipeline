from scripts.processing import DataQualityEngine
from scripts.bigquery_loader import BigQueryLoader
from scripts.config import RAW_DATA_PATH
from scripts.logger import logger


def stage_1_data_quality():
    """
    Executes the complete Data Quality Engine.
    """

    logger.info("========== Stage 1 : Data Quality ==========")

    engine = DataQualityEngine(RAW_DATA_PATH)

    engine.process()

    logger.info("Stage 1 Completed Successfully.")

    return engine


def stage_2_bigquery(engine):
    """
    Uploads cleaned data to BigQuery.
    """

    logger.info("========== Stage 2 : BigQuery Upload ==========")

    loader = BigQueryLoader()

    loader.run(engine.clean_df)

    logger.info("Stage 2 Completed Successfully.")


def run_pipeline():
    """
    Executes the complete pipeline.
    """

    logger.info("=======================================")
    logger.info("Customer Support Analytics Pipeline")
    logger.info("=======================================")

    engine = stage_1_data_quality()

    stage_2_bigquery(engine)

    logger.info("=======================================")
    logger.info("Pipeline Finished Successfully")
    logger.info("=======================================")


if __name__ == "__main__":
    run_pipeline()