import subprocess
import shutil
import time
import os
from logger import app_logger

class ErrorManager:
    def __init__(self):
        pass

    def handle_error(self, failing_command, error_type):
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

    def recovery_loop(self, failing_command, recovery_steps):
        for attempt in range(3):
            try:
                app_logger.log_info(f"Attempt {attempt + 1} for command.")
                failing_command()
                app_logger.log_info("Command executed successfully.")
                return
            except Exception as e:
                app_logger.log_error(f"Attempt {attempt + 1} failed: {e}")

                # Apply recovery steps
                for step in recovery_steps:
                    try:
                        app_logger.log_info(f"Executing recovery step: {step}")
                        step()
                    except Exception as recovery_error:
                        app_logger.log_error(f"Recovery step failed: {recovery_error}")
                time.sleep(2)  # Delay before retrying

        app_logger.log_error("All recovery attempts failed. Manual intervention required.")
        raise Exception("Recovery failed after 3 attempts.")

    def rebuild_cache(self):
        app_logger.log_info("Rebuilding npm cache...")
        subprocess.run(["npm", "cache", "clean", "--force"], check=True)

    def reinstall_dependencies(self):
        app_logger.log_info("Reinstalling npm dependencies...")
        if os.path.exists("package-lock.json"):
            os.remove("package-lock.json")
        if os.path.exists("node_modules"):
            shutil.rmtree("node_modules")
        subprocess.run(["npm", "install"], check=True)

    def check_permissions(self, file_path):
        app_logger.log_info(f"Fixing permissions for: {file_path}")
        subprocess.run(["chmod", "u+rw", file_path], check=True)

# Example usage
if __name__ == '__main__':
    error_manager = ErrorManager()
    try:
        error_manager.handle_error(lambda: subprocess.run(["npm", "install"], check=True), "missing_package_json")
    except Exception as e:
        app_logger.log_error(e)