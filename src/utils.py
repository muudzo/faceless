import logging
import sys
from pathlib import Path

def setup_logger(name="faceless_automation", log_file="pipeline.log"):
    """
    Sets up a logger that outputs to both console and a file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File handler
    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger

class PipelineError(Exception):
    """Custom exception for pipeline-related errors."""
    pass

def log_error(logger, message, e=None):
    """Logs an error message and the exception if provided."""
    if e:
        logger.error(f"{message}: {str(e)}")
    else:
        logger.error(message)

import time
from functools import wraps

def retry(exceptions, tries=3, delay=1, backoff=2, logger=None):
    """
    Retry decorator with exponential backoff.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            m_tries, m_delay = tries, delay
            while m_tries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = f"Retrying in {m_delay} seconds... (Error: {e})"
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(m_delay)
                    m_tries -= 1
                    m_delay *= backoff
            return f(*args, **kwargs)
        return wrapper
    return decorator
