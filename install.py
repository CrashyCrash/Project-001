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
