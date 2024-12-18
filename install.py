<<<<<<< HEAD
import subprocess
import sys
import os
from logger import MyLogger

logger = app_logger  # Updated from MyLogger

def install_requirements():
    """
    Installs required dependencies listed in requirements.txt.
    """
    try:
        logger.log_info("Starting installation of dependencies...")
        requirements_file = "requirements.txt"

        if not os.path.exists(requirements_file):
            logger.log_error(f"Missing {requirements_file}. Cannot install dependencies.", severity="critical")
            return

        # Run pip install
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        logger.log_info("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.log_critical(f"Failed to install dependencies: {e}")
    except Exception as e:
        logger.log_critical(f"Unexpected error during installation: {e}")

def create_virtual_environment(venv_path="venv"):
    """
    Creates a virtual environment if it does not already exist.
    """
    try:
        if not os.path.exists(venv_path):
            logger.log_info(f"Creating virtual environment at {venv_path}...")
            subprocess.check_call([sys.executable, "-m", "venv", venv_path])
            logger.log_info("Virtual environment created successfully.")
        else:
            logger.log_info(f"Virtual environment already exists at {venv_path}.")
    except Exception as e:
        logger.log_critical(f"Error creating virtual environment: {e}")

def activate_virtual_environment(venv_path="venv"):
    """
    Activates the virtual environment.
    """
    activate_script = os.path.join(venv_path, "bin", "activate")
    if sys.platform == "win32":
        activate_script = os.path.join(venv_path, "Scripts", "activate")

    if not os.path.exists(activate_script):
        logger.log_error(f"Activation script not found: {activate_script}", severity="critical")
        return False

    logger.log_info(f"Virtual environment ready at {venv_path}. Please activate it manually.")
    return True

if __name__ == "__main__":
    try:
        # Step 1: Create virtual environment
        create_virtual_environment()

        # Step 2: Install dependencies
        install_requirements()

        # Step 3: Prompt for manual activation
        activate_virtual_environment()

        logger.log_info("Installation script completed successfully.")
    except Exception as e:
        logger.log_critical(f"Unexpected error in install script: {e}")
=======
import os
import subprocess


def main():
    print("Creating virtual environment...")
    os.system("python3 -m venv venv")
    print("Activating virtual environment...")
    subprocess.run(["source", "venv/bin/activate"], shell=True)
    print("Installing dependencies...")
    os.system("pip install -r requirements.txt")
    print("Setup complete! Use launch.sh or launch.bat to run the project.")


if __name__ == "__main__":
    main()
>>>>>>> origin/main
