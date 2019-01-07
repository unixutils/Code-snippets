#!/usr/bin/python
import logging

# Create a logger
# the logger name is set to the name of the current module 
# __name__ is a built-in variable which evaluates to the name of the current module.
logger = logging.getLogger(__name__)

# Create handlers for stdout with custom log level, log format
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)
stdout_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(stdout_format)

# Create handlers for logging to files
file_handler = logging.FileHandler('application.log')
file_handler.setLevel(logging.ERROR)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(stdout_handler)
logger.addHandler(file_handler)

# set default to logger as well, not just for handlers
logger.setLevel(logging.DEBUG)

logger.error('Some error occured')
logger.info('Information')
