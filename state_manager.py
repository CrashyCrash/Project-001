import json
import os

class StateManager:
    def __init__(self, state_file="session_state.json"):
        self.state_file = state_file
        if not os.path.exists(state_file):
            self.save_state({"initialized": False})

    def load_state(self):
        with open(self.state_file, "r") as f:
            return json.load(f)

    def save_state(self, state):
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)