import json
import os

class StateManager:
    """
    A class to manage the state of the application by saving and loading it
    from a JSON file.
    """

    def __init__(self, state_file=None):
        """
        Initialize the StateManager with the path to the state file.
        If no state file is provided, it defaults to system_state.json in the logs directory.
        """
        self.state_file = state_file or '/Users/crashair/AI-Software/_Interpreter/Projects/Project-001/logs/system_state.json'
        self.state = {}
        self._initialize_state_file()

    def _initialize_state_file(self):
        """
        Ensure that the state file exists and has an initial state if it doesn't already.
        """
        if not os.path.exists(self.state_file):
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump({}, f)

    def load_state(self):
        """
        Load the state from the JSON file.
        """
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    self.state = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading state file: {e}. Resetting state.")
                self.state = {}
        else:
            print("State file not found. Starting with an empty state.")
            self.state = {}

    def save_state(self):
        """
        Save the current state to the JSON file.
        """
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=4)
            print("State successfully saved.")
        except Exception as e:
            print(f"Error saving state: {e}")

    def update_state(self, key, value):
        """
        Update a key-value pair in the state and save it to the file.
        """
        self.state[key] = value
        self.save_state()
        print(f"State updated: {key} = {value}")

    def get_state(self):
        """
        Retrieve the entire state as a dictionary.
        """
        return self.state

    def get_value(self, key):
        """
        Retrieve the value for a specific key in the state.
        """
        return self.state.get(key)

    def delete_key(self, key):
        """
        Delete a specific key from the state and save the updated state.
        """
        if key in self.state:
            del self.state[key]
            self.save_state()
            print(f"Deleted key: {key}")
        else:
            print(f"Key '{key}' not found in state.")

# Example usage
if __name__ == "__main__":
    state_manager = StateManager()
    state_manager.load_state()
    state_manager.update_state('initialized', True)
    print("Current state:", state_manager.get_state())