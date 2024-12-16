
from error_manager import ErrorManager

# Create an instance of ErrorManager
error_manager = ErrorManager()

# Define a command that raises a ValueError for testing
def faulty_command():
    raise ValueError('Simulated ValueError for testing.')

# Run the recovery loop with the faulty command
result = error_manager.recovery_loop(faulty_command)

# Print the result of the recovery attempt
print('Recovery was successful:', result)
