from loguru import logger

class Logger:
    def __init__(self, log_file="logs/log_output.log"):  # Updated path
        self.log_file = log_file
        self._setup_logging()

    def _setup_logging(self):
        logger.add(self.log_file, rotation="1 MB", retention="10 days", level="DEBUG")

    def log_info(self, message, context=None):
        """
        Log an informational message.
        :param message: The message to log.
        :param context: Optional context to include in the log message.
        """
        if context:
            logger.info(f"[{context}] {message}")
        else:
            logger.info(message)

    def log_error(self, message, context=None):
        """
        Log an error message.
        :param message: The message to log.
        :param context: Optional context to include in the log message.
        """
        if context:
            logger.error(f"[{context}] {message}")
        else:
            logger.error(message)

    def log_warning(self, message, context=None):
        """
        Log a warning message.
        :param message: The message to log.
        :param context: Optional context to include in the log message.
        """
        if context:
            logger.warning(f"[{context}] {message}")
        else:
            logger.warning(message)

# Global instance of the Logger
app_logger = Logger()