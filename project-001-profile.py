from logger import logger
from error_manager import ErrorManager
from env_manager import EnvironmentManager
from state_manager import StateManager

def main():
    base_dir = "/Users/crashair/AI-Software/_Interpreter/Projects/Project-001/"
    
    # Initialize managers
    error_manager = ErrorManager()  # No longer passing logger
    state_manager = StateManager()
    env_manager = EnvironmentManager(base_dir, logger, error_manager)

    # Log start of program
    logger.info("Starting Project-001 Profile...")

    # Check session state
    state_manager.load_state()
    if not state_manager.get_value("initialized"):
        logger.info("Environment not initialized. Setting it up now...")
        try:
            env_manager.setup_environment()
            state_manager.update_state("initialized", True)
            logger.info("Environment setup successfully completed.")
        except Exception as e:
            logger.error(f"An error occurred during environment setup: {e}")
            error_manager.handle_error(lambda: env_manager.setup_environment(), "failed_npm_install")
    
    # Main functionality placeholder
    logger.info("Running main functionality...")
    # Add any core application logic here

    logger.info("Project-001 Profile completed successfully.")

if __name__ == "__main__":
    main()