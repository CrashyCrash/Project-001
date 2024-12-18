import os
import sys
from loguru import logger

class CustomProfile:
    """
    Represents the main profile setup for Project-001.
    This class initializes the logger and provides the main execution flow.
    """

    def __init__(self):
        # Initialize loggers
        self._setup_loggers()
        logger.info("Custom profile initialized successfully.")

    def _setup_loggers(self):
        """
        Setup the loggers for the profile.
        """
        # Remove default logger and add a custom Loguru handler
        logger.remove()
        log_file_path = os.path.join(os.getcwd(), "custom_profile.log")
        logger.add(log_file_path, rotation="1 MB", level="INFO", backtrace=True, diagnose=True)
        logger.info("Loguru logger setup complete.")

    def run(self):
        """
        Entry point to execute the profile setup and main tasks.
        """
        logger.info("CustomProfile is starting the main tasks.")
        try:
            # Simulate main tasks or add actual tasks here
            print("Welcome to the custom profile execution.")
            self._main_loop()

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            sys.exit(1)

    def _main_loop(self):
        """
        Main loop for processing commands or actions.
        """
        while True:
            try:
                user_input = input("Enter a command (or 'exit' to quit): ")
                if user_input.lower() == 'exit':
                    logger.info("Exiting the custom profile.")
                    print("Goodbye!")
                    break
                else:
                    logger.info(f"Received command: {user_input}")
                    print(f"Command '{user_input}' received and processed.")
            except KeyboardInterrupt:
                logger.info("Custom profile interrupted by user.")
                print("\nInterrupted. Exiting gracefully.")
                break


if __name__ == "__main__":
    # Entry point when this script is run
    profile = CustomProfile()
    profile.run()