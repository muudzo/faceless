import sys
import re
from pathlib import Path

class SensitiveDataFilter(logging.Filter):
    """
    Redacts sensitive information like API keys from logs.
    """
    def filter(self, record):
        msg = str(record.msg)
        # Patterns for common API keys (Groq, Pexels, etc.)
        # Usually 30+ chars of alphanumeric/symbols
        patterns = [
            r'gsk_[a-zA-Z0-9]{30,}', # Groq
            r'[a-zA-Z0-9]{56}',     # Pexels (approx)
        ]
        for pattern in patterns:
            msg = re.sub(pattern, '[REDACTED]', msg)
        record.msg = msg
        return True

def setup_logger(name="faceless_automation", log_file="pipeline.log"):
    """
    Sets up a logger that outputs to both console and a file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.hasHandlers():
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        # Add security filter
        log_filter = SensitiveDataFilter()
        logger.addFilter(log_filter)
        
    return logger

class Sanitizer:
    """
    Utilities for cleaning and validating external string data.
    """
    @staticmethod
    def clean_text(text, max_len=2000):
        if not text:
            return ""
        # Strip HTML
        text = re.sub(r'<[^>]*>', '', text)
        # Strip non-printable characters
        text = "".join(char for char in text if char.isprintable())
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Truncate
        return text[:max_len]

    @staticmethod
    def sanitize_filename(name):
        return re.sub(r'[^a-zA-Z0-9._-]', '_', name)

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

def timeit(logger=None):
    """
    Performance profiling decorator.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = f(*args, **kwargs)
            end = time.perf_counter()
            elapsed = end - start
            msg = f"Function '{f.__name__}' took {elapsed:.4f} seconds"
            if logger:
                logger.info(msg)
            else:
                print(msg)
            return result
        return wrapper
    return decorator

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
