import os
import datetime

class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.activity_log = os.path.join(log_dir, "activity.log")
        self.error_log = os.path.join(log_dir, "error.log")

    def log(self, message, level="INFO"):
        log_file = self.activity_log if level == "INFO" else self.error_log
        timestamp = datetime.datetime.now().isoformat()
        with open(log_file, "a") as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")

    def log_info(self, message):
        self.log(message, "INFO")

    def log_error(self, message):
        self.log(message, "ERROR")