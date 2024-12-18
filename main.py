
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from custom_profile import CustomProfile  # Ensure custom_profile.py exists
from logger import Logger

# Initialize the logger
app_logger = app_logger

def main():
    """
    Main entry point to run the custom profile setup.
    """
    try:
        app_logger.log_info("Initializing Custom Profile...")
        profile = CustomProfile()
        profile.run()
    except Exception as e:
        app_logger.log_error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
