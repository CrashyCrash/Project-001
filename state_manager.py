import json
import os

class StateManager:
    def __init__(self):
        self.state_file = '/Users/crashair/AI-Software/_Interpreter/Projects/Project-001/logs/system_state.json'
        self.state = {}

    def update_state(self, key, value):
        self.state[key] = value
        self.save_state()
        print(f'State updated: {key} = {value}')

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {}

    def get_state(self):
        return self.state
