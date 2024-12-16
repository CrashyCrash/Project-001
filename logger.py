import logging
import os
from logging.handlers import RotatingFileHandler

LOG_FILENAME = '/Users/crashair/AI-Software/_Interpreter/Projects/Project-001/logs/app.log'

# Create a custom logger
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)

# Create handlers
file_handler = RotatingFileHandler(LOG_FILENAME, maxBytes=1e6, backupCount=5)
console_handler = logging.StreamHandler()

# Create formatters and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_info(message):
    logger.info(message)
def log_debug(message):
    logger.debug(message)
def log_warning(message):
    logger.warning(message)
def log_error(message):
    logger.error(message)
def log_critical(message):
    logger.critical(message)
