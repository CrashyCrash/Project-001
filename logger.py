import logging
import os
from loguru import logger

class Logger:
    """
    A class to set up and manage application logging using both Python's logging
    module and Loguru for advanced logging.
    """

    def __init__(self, log_dir="logs", log_file="app.log", log_level=logging.INFO):
        """
        Initialize the Logger with the specified directory and file for logs.
        If the directory does not exist, it will be created.
        """
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)
        self.log_level = log_level

        # Ensure the log directory exists
        os.makedirs(self.log_dir, exist_ok=True)

        # Set up Python logging
        self._setup_python_logger()

        # Set up Loguru logging
        self._setup_loguru_logger()

    def _setup_python_logger(self):
        """
        Configure the standard Python logging.
        """
        logging.basicConfig(
            level=self.log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger("MyLogger")
        self.logger.info("Python logger initialized.")

    def _setup_loguru_logger(self):
        """
        Configure the Loguru logger for more advanced logging.
        """
        loguru_file = os.path.join(self.log_dir, "loguru_app.log")
        logger.add(
            loguru_file,
            rotation="1 MB",
            compression="zip",
            format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}",
        )
        logger.info("Loguru logger initialized.")

    def log_info(self, message):
        """
        Log an informational message using both loggers.
        """
        self.logger.info(message)
        logger.info(message)

    def log_warning(self, message):
        """
        Log a warning message using both loggers.
        """
        self.logger.warning(message)
        logger.warning(message)

    def log_error(self, message):
        """
        Log an error message using both loggers.
        """
        self.logger.error(message)
        logger.error(message)

    def log_critical(self, message):
        """
        Log a critical error message using both loggers.
        """
        self.logger.critical(message)
        logger.critical(message)

# Example usage
if __name__ == "__main__":
    # Initialize the logger

    # Log various levels of messages
    app_logger.log_info("This is an informational message.")
    app_logger.log_warning("This is a warning message.")
    app_logger.log_error("This is an error message.")
    app_logger.log_critical("This is a critical error message.")
