class ErrorManager:
    def __init__(self, logger):
        # Ensure the logger is a Logger object
        if hasattr(logger, "log_error"):
            self.logger = logger
        else:
            raise ValueError("Logger instance is invalid or improperly initialized.")

    def handle_error(self, message, severity="Error", recovery_steps=None):
        """
        Handles errors by logging the error and optionally providing recovery steps.

        Args:
            message (str): The error message to log.
            severity (str): The severity level of the error (e.g., 'Error', 'Critical').
            recovery_steps (list): A list of recovery steps as strings.
        """
        # Log the error
        self.logger.log_error(f"{severity} Error: {message}")

        # Print recovery steps if provided
        if recovery_steps:
            self.logger.log_info("Suggested recovery steps:")
            for step in recovery_steps:
                self.logger.log_info(f" - {step}")

        # Optionally print to console for debugging
        print(f"[{severity}] {message}")
        if recovery_steps:
            print("Recovery steps:")
            for step in recovery_steps:
                print(f" - {step}")