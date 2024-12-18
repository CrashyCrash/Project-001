from error_manager import ErrorManager
from logger import app_logger

# Initialize custom logger


# Create an instance of ErrorManager
error_manager = ErrorManager()

# Define a command that raises a ValueError for testing
def faulty_command():
    raise ValueError('Simulated ValueError for testing.')

# Run the recovery loop with the faulty command
try:
    error_manager.recovery_loop(faulty_command, [lambda: "step1 executed", lambda: "step2 executed", lambda: "step3 executed"])
except Exception as e:
    app_logger.log_error(f"Error encountered: {str(e)}")

# Print the result of the recovery attempt
print('Recovery was successful:', False)
