import logging
import os

# ==========================================================
# Create logs directory
# ==========================================================

LOG_FOLDER = "logs"

os.makedirs(LOG_FOLDER, exist_ok=True)

# ==========================================================
# Configure logger
# ==========================================================

logging.basicConfig(
    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

    handlers=[
        logging.FileHandler(
            os.path.join(LOG_FOLDER, "pipeline.log")
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)