#!/usr/bin/python
import logging

# set log file name, log level and format of log entry, using logging.basicConfig() function.
logging.basicConfig(filename='application.log', level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')

# make sample log entries 
logging.debug(' this is a debug message')
logging.info('this is an info message')
logging.warn('this is a warn message')
logging.error('this is an error message')
logging.critical('this is a critical message')
