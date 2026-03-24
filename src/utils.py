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
