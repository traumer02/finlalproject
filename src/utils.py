import logging

# Configure the logging settings
logging.basicConfig(level=logging.INFO)

# Create a logger
logger = logging.getLogger(__name__)

# Log an informational message
logger.info("This is an informational message.")

# Additional log messages
# logger.debug("This is a debug message.")  # This won't be displayed because the logging level is set to INFO
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")