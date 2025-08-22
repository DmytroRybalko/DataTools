import logging
import os

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "process.log")

logging.basicConfig(
    filename=LOG_FILE,
    filemode='w',  # Overwrite the log file each run
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)