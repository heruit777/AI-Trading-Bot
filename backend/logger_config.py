import logging
import os

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging to store logs in logs/app.log
logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s",
    filename="logs/app.log",  # Store log in logs/app.log
    filemode="w",  # Append mode
)

# Create and export the logger
logger = logging.getLogger(__name__)
