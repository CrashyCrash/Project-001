from logger import app_logger
import requests
import flask
import click

# Initialize custom logger


# Use app_logger.log_info instead of direct loguru methods
app_logger.log_info("All required libraries are installed successfully.")
print("Flask version:", flask.__version__)
print("Requests version:", requests.__version__)
