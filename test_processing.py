from scripts.config import RAW_DATA_PATH

engine = DataQualityEngine(
    RAW_DATA_PATH
)

engine.process()