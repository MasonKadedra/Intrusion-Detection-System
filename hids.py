import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="hids.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_event(event_type, severity, source, description):
    """
    Logs a security event to hids.log
    """
    message = f"EventType={event_type} | Severity={severity} | Source={source} | Description={description}"
    if severity.lower() == "high":
        logging.error(message)
    elif severity.lower() == "medium":
        logging.warning(message)
    else:
        logging.info(message)

# Example usage
log_event("File Modified", "Medium", "/etc/passwd", "File hash mismatch detected")
log_event("SSH Brute Force", "High", "192.168.1.10", "5 failed login attempts within 2 minutes")
