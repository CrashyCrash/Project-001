import logging
from loguru import logger

class Logger:
    """
    A custom logger class that integrates both Loguru and Python's logging library.
    """
    _instance = None  # Singleton instance of Logger

    def __new__(cls, log_file="log_output.log"):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.log_file = log_file
            cls._instance.handlers = []  # Initialize handlers list
            cls._instance._setup_logging()
        return cls._instance

    def _setup_logging(self):
        # Configure Loguru
        logger.remove()  # Prevent duplicate handlers
        logger.add(self.log_file, rotation="1 MB", retention="10 days", level="DEBUG")
        self.handlers.append("Loguru Handler")

        # Configure Python logging
        logging.basicConfig(
            level=logging.DEBUG,
            filename=self.log_file,
            filemode='a',
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.handlers.append("Python Logging Handler")

    def log_info(self, message):
        logger.info(message)

    def log_error(self, message):
        logger.error(message)

    def log_debug(self, message):
        logger.debug(message)

# Global logger instance
app_logger = Logger()