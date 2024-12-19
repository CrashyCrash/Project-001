import os
import json
import subprocess
from logger import app_logger  # Correctly import app_logger
from error_manager import ErrorManager

class HealthCheck:
    """
    A utility to validate the integrity of key files, check permissions, and initiate recovery if necessary.
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.error_manager = ErrorManager()
        self.files_to_check = {
            "package.json": {
                "path": os.path.join(self.base_dir, "package.json"),
                "recovery_steps": [self.restore_package_json, self.create_package_json],
                "permissions": "644"  # rw-r--r--
            },
            "system_state.json": {
                "path": os.path.join(self.base_dir, "logs", "system_state.json"),
                "recovery_steps": [self.restore_system_state, self.initialize_system_state],
                "permissions": "644"  # rw-r--r--
            },
            "log_output.log": {
                "path": os.path.join(self.base_dir, "logs", "log_output.log"),  # Updated path
                "recovery_steps": [self.create_log_file],
                "permissions": "644"  # rw-r--r--
            },
            "config.txt": {
                "path": os.path.join(self.base_dir, "configs", "config.txt"),
                "recovery_steps": [self.create_config_txt],
                "permissions": "644"  # rw-r--r--
            },
            "setup.sh": {
                "path": os.path.join(self.base_dir, "scripts", "setup.sh"),
                "recovery_steps": [self.create_setup_sh],
                "permissions": "755"  # rwxr-xr-x
            }
        }
        self.recovery_summary = []  # Track recovery actions for reporting

    def validate_file(self, file_path):
        """
        Validate the integrity of a file.
        :param file_path: Path to the file to validate.
        :return: True if the file is valid, False otherwise.
        """
        if not os.path.exists(file_path):
            app_logger.log_error(f"File not found: {file_path}", context="HealthCheck")
            return False
        try:
            if file_path.endswith(".json"):
                with open(file_path, 'r') as f:
                    json.load(f)  # Validate JSON format
            elif file_path.endswith((".txt", ".sh", ".py")):
                with open(file_path, 'r') as f:
                    f.read()  # Validate readability
            app_logger.log_info(f"File validated: {file_path}", context="HealthCheck")
            return True
        except (json.JSONDecodeError, IOError) as e:
            app_logger.log_error(f"File corrupted: {file_path} - {e}", context="HealthCheck")
            return False

    def check_permissions(self, file_path, expected_permissions):
        """
        Check file permissions and fix them if necessary.
        :param file_path: Path to the file.
        :param expected_permissions: Expected permissions in octal format (e.g., "644").
        :return: True if permissions are correct, False otherwise.
        """
        try:
            current_permissions = oct(os.stat(file_path).st_mode)[-3:]
            if current_permissions != expected_permissions:
                app_logger.log_warning(f"Incorrect permissions for {file_path}. Expected: {expected_permissions}, Found: {current_permissions}", context="HealthCheck")
                self.fix_permissions(file_path, expected_permissions)
                return False
            app_logger.log_info(f"Permissions validated for {file_path}", context="HealthCheck")
            return True
        except FileNotFoundError:
            app_logger.log_error(f"File not found: {file_path}", context="HealthCheck")
            return False

    def fix_permissions(self, file_path, expected_permissions):
        """
        Fix file permissions to match the expected value.
        :param file_path: Path to the file.
        :param expected_permissions: Expected permissions in octal format (e.g., "644").
        """
        try:
            os.chmod(file_path, int(expected_permissions, 8))
            app_logger.log_info(f"Permissions fixed for {file_path} to {expected_permissions}", context="HealthCheck")
            self.recovery_summary.append(f"Fixed permissions for {file_path} to {expected_permissions}")
        except Exception as e:
            app_logger.log_error(f"Failed to fix permissions for {file_path}: {e}", context="HealthCheck")

    def run_health_check(self):
        """
        Run a health check on core files, check permissions, and initiate recovery if necessary.
        """
        for file_name, file_info in self.files_to_check.items():
            file_path = file_info["path"]
            valid = self.validate_file(file_path)
            if not valid:
                app_logger.log_error(f"File validation failed for {file_name}. Initiating recovery.", context="HealthCheck")
                self.recovery_summary.append(f"File validation failed for {file_name}")
                self.error_manager.recovery_loop(
                    failing_command=lambda: None,
                    recovery_steps=file_info["recovery_steps"]
                )
            # Check and fix permissions
            if not self.check_permissions(file_path, file_info.get("permissions", "644")):
                self.recovery_summary.append(f"Permissions checked for {file_name}")

        # Output recovery summary
        self.output_recovery_summary()

    def output_recovery_summary(self):
        """
        Output a summary of actions taken during the health check.
        """
        if self.recovery_summary:
            app_logger.log_info("Recovery Summary:", context="HealthCheck")
            for action in self.recovery_summary:
                app_logger.log_info(f"- {action}", context="HealthCheck")
        else:
            app_logger.log_info("No recovery actions were necessary. All files are healthy.", context="HealthCheck")

    def restore_package_json(self):
        """
        Restore package.json from a backup if available.
        """
        backup_path = os.path.join(self.base_dir, "package.json.backup")
        if os.path.exists(backup_path):
            os.replace(backup_path, self.files_to_check["package.json"]["path"])
            app_logger.log_info("Restored package.json from backup.", context="HealthCheck")
            self.recovery_summary.append("Restored package.json from backup")
        else:
            app_logger.log_warning("No backup found for package.json.", context="HealthCheck")

    def create_package_json(self):
        """
        Create a new package.json with a minimal valid structure.
        """
        with open(self.files_to_check["package.json"]["path"], 'w') as f:
            json.dump({"name": "project", "version": "1.0.0"}, f, indent=4)
        app_logger.log_info("Created new package.json.", context="HealthCheck")
        self.recovery_summary.append("Created new package.json")

    def restore_system_state(self):
        """
        Restore system_state.json from a backup if available.
        """
        backup_path = os.path.join(self.base_dir, "logs", "system_state.json.backup")
        if os.path.exists(backup_path):
            os.replace(backup_path, self.files_to_check["system_state.json"]["path"])
            app_logger.log_info("Restored system_state.json from backup.", context="HealthCheck")
            self.recovery_summary.append("Restored system_state.json from backup")
        else:
            app_logger.log_warning("No backup found for system_state.json.", context="HealthCheck")

    def initialize_system_state(self):
        """
        Initialize system_state.json with an empty state.
        """
        with open(self.files_to_check["system_state.json"]["path"], 'w') as f:
            json.dump({}, f, indent=4)
        app_logger.log_info("Initialized system_state.json with empty state.", context="HealthCheck")
        self.recovery_summary.append("Initialized system_state.json with empty state")

    def create_log_file(self):
        """
        Create a new log_output.log file if it doesn't exist.
        """
        if not os.path.exists(self.files_to_check["log_output.log"]["path"]):
            with open(self.files_to_check["log_output.log"]["path"], 'w') as f:
                f.write("")
            app_logger.log_info("Created new log_output.log.", context="HealthCheck")
            self.recovery_summary.append("Created new log_output.log")

    def create_config_txt(self):
        """
        Create a new config.txt file with default content.
        """
        if not os.path.exists(self.files_to_check["config.txt"]["path"]):
            with open(self.files_to_check["config.txt"]["path"], 'w') as f:
                f.write("Default configuration")
            app_logger.log_info("Created new config.txt.", context="HealthCheck")
            self.recovery_summary.append("Created new config.txt")

    def create_setup_sh(self):
        """
        Create a new setup.sh script with default content.
        """
        if not os.path.exists(self.files_to_check["setup.sh"]["path"]):
            with open(self.files_to_check["setup.sh"]["path"], 'w') as f:
                f.write("#!/bin/bash\n# Default setup script")
            os.chmod(self.files_to_check["setup.sh"]["path"], 0o755)  # Set executable permissions
            app_logger.log_info("Created new setup.sh.", context="HealthCheck")
            self.recovery_summary.append("Created new setup.sh")

# Example usage
if __name__ == "__main__":
    base_dir = "/Users/crashair/AI-Software/_Interpreter/Projects/Project-001"
    health_check = HealthCheck(base_dir)
    health_check.run_health_check()