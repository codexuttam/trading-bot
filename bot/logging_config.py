import logging
import os
from datetime import datetime

# Ensure logs directory exists
LOG_DIR = os.path.join(os.getcwd(), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file path
LOG_FILE = os.path.join(LOG_DIR, f"trading_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def setup_logging():
    """Sets up unified logging for both console and file."""
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.INFO)

    # Prevent potential duplicate loggers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console Handler (Optional, as Click/Rich handles console mostly)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()
