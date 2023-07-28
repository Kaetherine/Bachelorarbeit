import logging
from helpers import csv_path as path_to_logfile

def setup_logger():
    '''Logger konfigurieren und Instanz zurückgeben'''
    logging.basicConfig(
        filename=f'{path_to_logfile}logfile.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
        )
    logger = logging.getLogger('logger1')
    return logger
