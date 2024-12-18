import os
import subprocess
from logger import Logger
from error_manager import ErrorManager

class EnvironmentManager:
    """
    A class to manage environment setup, including directory creation, version checks,
    and dependency installations.
    """

    def __init__(self, base_dir, logger, error_manager):
        """
        Initialize the EnvironmentManager with the project directory, logger, and error manager.
        """
        self.base_dir = base_dir
        self.logger = logger
        self.error_manager = error_manager
        self.directories = ["logs", "src", "build", "configs"]

    def setup_environment(self):
        """
        Perform the full environment setup process.
        """
        try:
            self.logger.log_info("Starting environment setup...", context="EnvironmentManager")

            # Step 1: Create required directories
            self._create_directories()

            # Step 2: Check Node.js, npm, and Python versions
            self._check_versions()

            # Step 3: Install dependencies if necessary
            self._install_dependencies()

            self.logger.log_info("Environment setup complete.", context="EnvironmentManager")
            print("Environment setup complete.")

        except Exception as e:
            self.logger.log_error(f"Environment setup failed: {e}", context="EnvironmentManager")
            self.error_manager.handle_error(
                failing_command=lambda: None,
                error_type="setup_failure"
            )

    def _create_directories(self):
        """
        Create the required directories for the project.
        """
        self.logger.log_info("Creating project directories...", context="EnvironmentManager")
        for directory in self.directories:
            path = os.path.join(self.base_dir, directory)
            os.makedirs(path, exist_ok=True)
            self.logger.log_info(f"Created directory: {path}", context="EnvironmentManager")

    def _check_versions(self):
        """
        Check that Node.js, npm, and Python are installed and print their versions.
        """
        self.logger.log_info("Checking Node.js, npm, and Python versions...", context="EnvironmentManager")

        # Node.js
        node_version = self._run_command(["node", "-v"], "Node.js not found.")
        self.logger.log_info(f"Node.js version: {node_version}", context="EnvironmentManager")

        # npm
        npm_version = self._run_command(["npm", "-v"], "npm not found.")
        self.logger.log_info(f"npm version: {npm_version}", context="EnvironmentManager")

        # Python
        python_version = self._run_command(["python3", "--version"], "Python not found.")
        self.logger.log_info(f"Python version: {python_version}", context="EnvironmentManager")

    def _install_dependencies(self):
        """
        Install npm dependencies if package.json exists.
        """
        package_json_path = os.path.join(self.base_dir, "package.json")
        node_modules_path = os.path.join(self.base_dir, "node_modules")

        if os.path.exists(package_json_path):
            self.logger.log_info("package.json found. Checking dependencies...", context="EnvironmentManager")
            if not os.path.exists(node_modules_path):
                self.logger.log_info("Installing npm dependencies...", context="EnvironmentManager")
                result = subprocess.run(
                    ["npm", "install"],
                    cwd=self.base_dir,
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    self.logger.log_info("Dependencies installed successfully.", context="EnvironmentManager")
                else:
                    self.logger.log_error(f"npm install failed: {result.stderr}", context="EnvironmentManager")
                    raise Exception("npm install failed. Check error logs for details.")
            else:
                self.logger.log_info("Dependencies already installed (node_modules exists).", context="EnvironmentManager")
        else:
            self.logger.log_warning("package.json not found. Skipping dependency installation.", context="EnvironmentManager")

    def _run_command(self, command, error_message):
        """
        Run a shell command and return its output. Raise an error if it fails.
        :param command: The command to run (list of arguments).
        :param error_message: The error message to log if the command fails.
        :return: The output of the command.
        """
        try:
            result = subprocess.run(command, cwd=self.base_dir, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            self.logger.log_error(error_message, context="EnvironmentManager")
            raise Exception(error_message)

# Example usage
if __name__ == "__main__":
    # Set up paths
    base_dir = "/Users/crashair/AI-Software/_Interpreter/Projects/Project-001"

    # Ensure logs directory exists
    os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)

    # Initialize Logger and ErrorManager
    logger = Logger()
    error_manager = ErrorManager()

    # Run EnvironmentManager
    env_manager = EnvironmentManager(base_dir, logger, error_manager)
    env_manager.setup_environment()