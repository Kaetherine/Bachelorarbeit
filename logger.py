import logging

def setup_logger():
    '''Logger konfigurieren und Instanz zurückgeben'''
    logging.basicConfig(
        filename='logfile.log',
        level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
        )
    logger = logging.getLogger('mein_logger')
    return logger
