from logger import app_logger
from error_manager import ErrorManager

app_logger.log_info("Logger is initialized.")

error_manager = ErrorManager()

def faulty_command():
    raise ValueError('Simulated ValueError for testing.')

try:
    error_manager.recovery_loop(
        faulty_command,
        [
            error_manager.create_package_json,  # Use named functions
            error_manager.rebuild_cache,
            error_manager.reinstall_dependencies
        ]
    )
    print("Recovery was successful:", True)
except Exception as e:
    app_logger.log_error(f"Error encountered: {str(e)}")
    print("Recovery was successful:", False)