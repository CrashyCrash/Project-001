from loguru import logger
import requests
import flask
import click

logger.info("All required libraries are installed successfully.")
print("Flask version:", flask.__version__)
print("Requests version:", requests.__version__)