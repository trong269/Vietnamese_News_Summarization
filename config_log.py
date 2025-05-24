import logging.config
import os

log_file_path = 'logging.log'

logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    filemode='a', 
    encoding='utf-8',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger