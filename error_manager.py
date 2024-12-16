import subprocess
import os
import logging
import shutil
import time
from loguru import logger


class ErrorManager:
    """
    A class to manage error handling, categorization, and recovery.
    """

    def __init__(self, log_dir="logs"):
        """
        Initialize the ErrorManager with a default or custom log directory.
        """
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "error.log")
        logger.add(log_path, rotation="1 MB", compression="zip")
        self.logger = logger
        self.retry_count = 0

    def log_error(self, error, severity="ERROR"):
        """
        Logs errors into a file with the specified severity.
        """
        self.logger.log(severity, error)

    def categorize_error(self, error):
        """
        Categorizes errors into Minor, Moderate, and Critical.
        """
        if isinstance(error, FileNotFoundError):
            return "Minor"
        elif isinstance(error, PermissionError):
            return "Moderate"
        elif isinstance(error, subprocess.CalledProcessError):
            return "Critical"
        else:
            return "Unknown"

    def recovery_loop(self, failing_command, recovery_steps):
        """
        Attempts to run the failing command and apply recovery steps upon failure.
        """
        for attempt in range(1, 4):  # Retry up to 3 times
            try:
                self.logger.info(f"Attempting command: {failing_command}")
                failing_command()  # Execute the command
                self.logger.info("Command succeeded.")
                return
            except subprocess.CalledProcessError as e:
                
        log_error("Error occurred while attempting recovery: {e}")(f"Subprocess failed with error: {e}")
                self.log_error(e)
                self.logger.info(f"Attempt {attempt} of 3 failed. Applying recovery steps.")

                # Apply recovery steps
                for step in recovery_steps:
                    try:
                        self.logger.debug(f"Executing recovery step: {step}")
                        step()
                    except Exception as recovery_error:
                        
        log_error("Error occurred while attempting recovery: {e}")(f"Recovery step failed: {recovery_error}")
                time.sleep(2)  # Delay before retrying

        self.logger.critical("All recovery attempts failed. Manual intervention required.")
        raise Exception("Recovery failed after 3 attempts.")

    def rebuild_cache(self):
        """Rebuilds npm cache."""
        self.logger.info("Rebuilding npm cache...")
        subprocess.run(["npm", "cache", "clean", "--force"], check=True)

    def reinstall_dependencies(self):
        """Reinstalls npm dependencies."""
        self.logger.info("Reinstalling npm dependencies...")
        if os.path.exists("package-lock.json"):
            os.remove("package-lock.json")
        if os.path.exists("node_modules"):
            shutil.rmtree("node_modules")
        subprocess.run(["npm", "install"], check=True)

    def check_permissions(self, file_path):
        """Fixes file permission issues."""
        self.logger.info(f"Fixing permissions for: {file_path}")
        subprocess.run(["chmod", "u+rw", file_path], check=True)

    def handle_error(self, failing_command, error_type):
        """
        High-level error handler for predefined error types.
        """
        recovery_steps = []

        if error_type == "missing_package_json":
            recovery_steps = [lambda: open("package.json", "w").close()]
        elif error_type == "failed_npm_install":
            recovery_steps = [
                lambda: self.rebuild_cache(),
                lambda: self.reinstall_dependencies(),
            ]
        elif error_type == "corrupted_package_json":
            recovery_steps = [
                lambda: self.rebuild_cache(),
                lambda: self.reinstall_dependencies(),
            ]
        elif error_type == "network_error":
            recovery_steps = [lambda: time.sleep(10)]
        elif error_type == "permission_error":
            recovery_steps = [lambda: self.check_permissions("package.json")]

        self.recovery_loop(failing_command, recovery_steps)


# Example Usage:
if __name__ == "__main__":
    manager = ErrorManager()

    try:
        # Simulate a missing package.json
        manager.handle_error(lambda: subprocess.run(["npm", "install"], check=True), "missing_package_json")
    except Exception as e:
        manager.log_error(e)