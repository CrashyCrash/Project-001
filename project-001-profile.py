from logger import Logger
from error_manager import ErrorManager
from env_manager import EnvironmentManager
from state_manager import StateManager

def main():
    base_dir = "/Users/crashair/AI-Software/_Interpreter/Projects/Project-001/"
    logger = Logger()
    error_manager = ErrorManager(logger)
    state_manager = StateManager()
    env_manager = EnvironmentManager(base_dir, logger, error_manager)

    # Check session state
    state = state_manager.load_state()
    if not state.get("initialized"):
        env_manager.setup_environment()
        state["initialized"] = True
        state_manager.save_state(state)
        logger.log_info("Environment setup successfully completed.")

if __name__ == "__main__":
    main()