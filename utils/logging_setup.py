"""
Logging setup module.

This module configures the application's logging system.
"""

import logging
import os

# Default log file
LOG_FILE = "finding_excellence.log"

def setup_logging(log_file=LOG_FILE, level=logging.INFO):
    """
    Set up logging for the application.
    
    Args:
        log_file: Path to the log file
        level: Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    # Configure basic logging
    logging.basicConfig(
        filename=log_file,
        level=level,
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create a logger for the application
    logger = logging.getLogger('finding_excellence')
    
    # Add console handler if not already added
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(levelname)s: %(message)s'
        ))
        logger.addHandler(console_handler)
    
    return logger
