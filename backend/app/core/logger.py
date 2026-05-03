import logging
import sys

def setup_logger():
    logger = logging.getLogger("operon")
    logger.setLevel(logging.INFO)
    
    # Avoid adding multiple handlers if already setup
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(module)s | %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

logger = setup_logger()
