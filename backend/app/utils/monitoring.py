from app.core.logger import logger

def log_event(event_name: str, metadata: dict = None):
    meta_str = f" | metadata={metadata}" if metadata else ""
    logger.info(f"EVENT: {event_name}{meta_str}")

def log_error(error_name: str, metadata: dict = None):
    meta_str = f" | metadata={metadata}" if metadata else ""
    logger.error(f"ERROR: {error_name}{meta_str}")
