import logging
import os

LOG_FILE = os.path.join(r"C:\DimDev\DataTools\Read_BIN", "process.log")
logging.basicConfig(
    filename=LOG_FILE,
    filemode='w',  # Overwrite the log file each run
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)