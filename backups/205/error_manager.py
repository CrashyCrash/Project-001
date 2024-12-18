import json
import subprocess
import shutil
import time
import os
from logger import app_logger

class ErrorManager:
    def __init__(self):
        self.recovery_step_status = {}  # Track status of recovery steps

    def handle_error(self, failing_command, error_type):
        """
        Handles errors by attempting recovery steps.
        :param failing_command: The command that failed (must be callable).
        :param error_type: The type of error to handle.
        """
        if not callable(failing_command):
            raise ValueError("failing_command must be a callable function.")

        recovery_steps = self._get_recovery_steps(error_type)
        if not recovery_steps:
            raise ValueError(f"No recovery steps defined for error type: {error_type}")

        success = self.recovery_loop(failing_command, recovery_steps)
        if not success:
            app_logger.log_error("Recovery failed after all attempts.")
            raise Exception("Recovery process failed.")

    def _get_recovery_steps(self, error_type):
        """
        Returns the appropriate recovery steps based on the error type.
        :param error_type: The type of error to handle.
        :return: A list of recovery steps (callable functions).
        """
        recovery_steps = []

        if error_type == "missing_package_json":
            recovery_steps = [self.create_package_json]
        elif error_type == "failed_npm_install":
            recovery_steps = [self.rebuild_cache, self.reinstall_dependencies]
        elif error_type == "corrupted_package_json":
            recovery_steps = [self.rebuild_cache, self.reinstall_dependencies]
        elif error_type == "network_error":
            recovery_steps = [self.wait_for_network]
        elif error_type == "permission_error":
            recovery_steps = [lambda: self.check_permissions("package.json")]

        return recovery_steps

    def recovery_loop(self, failing_command, recovery_steps):
        """
        Attempts to execute the failing command multiple times, applying recovery steps between attempts.
        :param failing_command: The command that failed (must be callable).
        :param recovery_steps: A list of recovery steps (callable functions).
        :return: True if the command succeeds, False otherwise.
        """
        for attempt in range(3):
            try:
                app_logger.log_info(f"Attempt {attempt + 1} to execute the command.")
                failing_command()
                app_logger.log_info("Command executed successfully.")
                return True
            except Exception as e:
                app_logger.log_error(f"Attempt {attempt + 1} failed: {e}")
                for step in recovery_steps:
                    step_name = step.__name__ if hasattr(step, '__name__') else str(step)
                    if step_name not in self.recovery_step_status or not self.recovery_step_status[step_name]:
                        try:
                            app_logger.log_info(f"Executing recovery step: {step_name}")
                            step()
                            self.recovery_step_status[step_name] = True  # Mark step as successful
                        except Exception as recovery_error:
                            app_logger.log_error(f"Recovery step failed: {recovery_error}")
                            self.recovery_step_status[step_name] = False  # Mark step as failed
                    else:
                        app_logger.log_info(f"Skipping recovery step: {step_name} (already executed successfully)")
                app_logger.log_info("Retrying...")
                time.sleep(2)

        app_logger.log_error("All recovery attempts failed.")
        return False

    def create_package_json(self):
        """
        Creates a package.json file with a minimal valid JSON structure if it doesn't already exist.
        """
        if not os.path.exists("package.json"):
            app_logger.log_info("Creating package.json...")
            with open("package.json", "w") as f:
                json.dump({"name": "project", "version": "1.0.0"}, f, indent=4)
        else:
            app_logger.log_info("package.json already exists. Skipping creation.")

    def rebuild_cache(self):
        """
        Rebuilds the npm cache.
        """
        app_logger.log_info("Rebuilding npm cache...")
        try:
            subprocess.run(["npm", "cache", "clean", "--force"], check=True)
        except subprocess.CalledProcessError as e:
            app_logger.log_error(f"Failed to rebuild npm cache: {e}")
            raise

    def reinstall_dependencies(self):
        """
        Reinstalls npm dependencies.
        """
        app_logger.log_info("Reinstalling npm dependencies...")
        try:
            if os.path.exists("package-lock.json"):
                os.remove("package-lock.json")
            if os.path.exists("node_modules"):
                shutil.rmtree("node_modules")
            subprocess.run(["npm", "install"], check=True)
        except subprocess.CalledProcessError as e:
            app_logger.log_error(f"Failed to reinstall npm dependencies: {e}")
            raise

    def wait_for_network(self):
        """
        Waits for the network to become available.
        """
        app_logger.log_info("Waiting for network...")
        time.sleep(10)

    def check_permissions(self, file_path):
        """
        Fixes permissions for a given file.
        :param file_path: The path to the file to fix permissions for.
        """
        app_logger.log_info(f"Fixing permissions for: {file_path}")
        try:
            subprocess.run(["chmod", "u+rw", file_path], check=True)
        except subprocess.CalledProcessError as e:
            app_logger.log_error(f"Failed to fix permissions for {file_path}: {e}")
            raise

# Example usage
if __name__ == '__main__':
    error_manager = ErrorManager()
    try:
        error_manager.handle_error(
            failing_command=lambda: subprocess.run(["npm", "install"], check=True),
            error_type="missing_package_json"
        )
    except Exception as e:
        app_logger.log_error(f"Error encountered: {e}")