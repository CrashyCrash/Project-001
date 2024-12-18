import unittest
import os
from logger import app_logger
from state_manager import StateManager

class TestEnvironmentManager(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()
        self.state_manager.load_state()
        self.state_manager.update_state('test_key', 'initial_state')
        self.package_json = '/Users/crashair/AI-Software/_Interpreter/Projects/Project-001/package.json'

    def test_logging_on_error(self):
        try:
            raise ValueError('Test error for logging')
        except ValueError as e:
            app_logger.log_error(f'Test failed: {str(e)}')
            self.assertTrue(os.path.exists('/Users/crashair/AI-Software/_Interpreter/Projects/Project-001/log_output.log'))

    def test_state_update(self):
        self.state_manager.update_state('test_key', 'updated_state')
        self.assertEqual(self.state_manager.state['test_key'], 'updated_state')
        self.assertTrue(os.path.exists(self.state_manager.state_file))

if __name__ == '__main__':
    unittest.main()