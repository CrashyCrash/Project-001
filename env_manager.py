import os
import subprocess

class EnvironmentManager:
    def __init__(self, base_dir, logger, error_manager):
        self.base_dir = base_dir
        self.logger = logger
        self.error_manager = error_manager
        self.directories = ["logs", "src", "build", "configs"]

    def setup_environment(self):
        try:
            print("Starting environment setup...")
            self.logger.log_info("Starting environment setup...")

            # Step 1: Create standard directories
            for dir_name in self.directories:
                dir_path = os.path.join(self.base_dir, dir_name)
                print(f"Creating directory: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)
                self.logger.log_info(f"Directory created: {dir_path}")

            # Step 2: Check Node.js, npm, and Python versions
            print("Checking versions...")
            self._check_versions()

            # Step 3: Install dependencies if needed
            package_json_path = os.path.join(self.base_dir, "package.json")
            node_modules_path = os.path.join(self.base_dir, "node_modules")
            print("Looking for package.json and node_modules...")

            if os.path.exists(package_json_path):
                print("package.json found.")
                if not os.path.exists(node_modules_path):
                    print("node_modules not found. Running npm install...")
                    result = subprocess.run(
                        "npm install --verbose --force",
                        shell=True,
                        cwd=self.base_dir,
                        capture_output=True,
                        text=True
                    )
                    # Log outputs
                    print("npm install completed.")
                    if result.stdout:
                        self.logger.log_info(f"npm install output:\n{result.stdout}")
                    if result.stderr:
                        self.logger.log_error(f"npm install errors:\n{result.stderr}")
                    if result.returncode != 0:
                        raise Exception("npm install failed. Check error logs for details.")
                    self.logger.log_info("Dependencies installed successfully.")
                else:
                    print("node_modules already exists. Skipping npm install.")
                    self.logger.log_info("Dependencies already installed (node_modules exists).")
            else:
                print("package.json not found; skipping npm install.")
                self.logger.log_info("No package.json found; skipping npm install.")

            self.logger.log_info("Environment setup complete.")
            print("Environment setup complete.")

        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            self.error_manager.handle_error(
                str(e),
                severity="Critical",
                recovery_steps=[
                    "Ensure Node.js and npm are installed correctly.",
                    "Run 'npm install' manually if the script fails.",
                    "Check the package.json file exists and is valid."
                ]
            )

    def _check_versions(self):
        try:
            # Check Node.js version
            node_version = subprocess.run("node -v", shell=True, capture_output=True, text=True)
            if node_version.returncode != 0:
                raise Exception("Node.js not found.")
            self.logger.log_info(f"Node.js version: {node_version.stdout.strip()}")

            # Check npm version
            npm_version = subprocess.run("npm -v", shell=True, capture_output=True, text=True)
            if npm_version.returncode != 0:
                raise Exception("npm not found.")
            self.logger.log_info(f"npm version: {npm_version.stdout.strip()}")

            # Check Python version
            python_version = subprocess.run("python3 --version", shell=True, capture_output=True, text=True)
            if python_version.returncode != 0:
                raise Exception("Python not found.")
            self.logger.log_info(f"Python version: {python_version.stdout.strip()}")

        except Exception as e:
            raise Exception(f"Version check failed: {str(e)}")

if __name__ == "__main__":
    from logger import Logger
    from error_manager import ErrorManager

    # Ensure the logs directory exists for logging
    base_dir = "/Users/crashair/AI-Software/_Interpreter/Projects/Project-001"
    os.makedirs(os.path.join(base_dir, "logs"), exist_ok=True)

    # Initialize logger and error manager
    logger = Logger()
    error_manager = ErrorManager(logger)

    # Run the environment manager
    env_manager = EnvironmentManager(base_dir, logger, error_manager)
    env_manager.setup_environment()