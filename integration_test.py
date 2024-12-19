import os
import unittest
from logger import app_logger  # Correctly import app_logger
from error_manager import ErrorManager
from state_manager import StateManager
from env_manager import EnvironmentManager

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        # Initialize core modules
        self.base_dir = "/Users/crashair/AI-Software/_Interpreter/Projects/Project-001"
        self.state_manager = StateManager()
        self.error_manager = ErrorManager()
        self.env_manager = EnvironmentManager(self.base_dir, app_logger, self.error_manager)

        # Ensure logs directory exists
        os.makedirs(os.path.join(self.base_dir, "logs"), exist_ok=True)

        # Load initial state
        self.state_manager.load_state()

    def test_environment_setup_and_state_persistence(self):
        """
        Test the full environment setup process and ensure state is persisted correctly.
        """
        app_logger.log_info("Starting integration test: Environment setup and state persistence.")

        # Step 1: Run environment setup
        self.env_manager.setup_environment()

        # Step 2: Validate directories were created
        for directory in self.env_manager.directories:
            path = os.path.join(self.base_dir, directory)
            self.assertTrue(os.path.exists(path), f"Directory {path} should exist after setup.")

        # Step 3: Update state and save
        self.state_manager.update_state('environment_setup', True)
        self.assertTrue(self.state_manager.get_value('environment_setup'), "State should reflect environment setup.")

        # Step 4: Reload state and validate
        self.state_manager.load_state()
        self.assertTrue(self.state_manager.get_value('environment_setup'), "State should persist after reload.")

    def test_error_handling_and_recovery(self):
        """
        Test error handling and recovery processes.
        """
        app_logger.log_info("Starting integration test: Error handling and recovery.")

        # Simulate a missing package.json file
        package_json_path = os.path.join(self.base_dir, "package.json")
        if os.path.exists(package_json_path):
            os.remove(package_json_path)

        # Define a faulty command that checks for the existence of package.json
        def faulty_command():
            if not os.path.exists(package_json_path):
                raise FileNotFoundError("package.json is missing.")

        # Step 1: Run recovery loop with faulty command
        recovery_steps = [
            self.error_manager.create_package_json,
            self.error_manager.rebuild_cache,
            self.error_manager.reinstall_dependencies
        ]
        success = self.error_manager.recovery_loop(faulty_command, recovery_steps)

        # Step 2: Validate recovery status
        self.assertTrue(success, "Recovery should be successful after applying steps.")

        # Step 3: Verify that package.json was created
        self.assertTrue(os.path.exists(package_json_path), "package.json should exist after recovery.")

    def test_runtime_exception_recovery(self):
        """
        Test recovery for runtime exceptions.
        """
        app_logger.log_info("Starting integration test: Runtime exception recovery.")

        # Simulate a runtime exception
        def faulty_command():
            if not os.path.exists("temp_runtime_exception.txt"):
                raise ValueError("Simulated runtime exception.")

        # Step 1: Run recovery loop with faulty command
        recovery_steps = [
            self.error_manager.handle_runtime_exception
        ]
        success = self.error_manager.recovery_loop(faulty_command, recovery_steps)

        # Step 2: Validate recovery status
        self.assertTrue(success, "Recovery should be successful after applying steps.")

        # Step 3: Verify that the recovery logic executed successfully
        temp_file = "temp_runtime_exception.txt"
        self.assertTrue(os.path.exists(temp_file), f"Temporary file {temp_file} should exist after recovery.")

    def tearDown(self):
        # Clean up state after tests
        self.state_manager.delete_key('environment_setup')
        self.state_manager.save_state()

if __name__ == '__main__':
    unittest.main()