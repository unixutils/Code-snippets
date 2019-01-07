#!/usr/bin/python
import logging
import sys

logging.basicConfig(filename='application.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


try:
    employee_name = sys.argv[1]
    employee_age  = int(sys.argv[2])
    application_status = sys.argv[3]
    enrollment_list = []
except Exception as e:
    logging.exception("Exception occurred", exc_info=True)

def my_function():
  logger = logging.getLogger(__name__)
  if application_status == "failed":
     print "Enrollment failed since application status is failed"
     logger.error('Enrollment failed for: %s', employee_name)
  elif employee_age > 55 and application_status == 'passed':
     enrollment_list.append(employee_name+':'+str(employee_age)+':'+application_status)
     logger.warn('Enrollment successful for: %s', employee_name)
     logger.warn('age is above threshold')
  elif employee_age < 55 and application_status == 'passed':
     enrollment_list.append(employee_name+':'+str(employee_age)+':'+application_status)
     logger.info('Enrollment successful for: %s', employee_name)
  else:
     print "Critical application error, unknown application status"
     logger.critical('Enrollment failed for: %s', employee_name)
     logger.critical('Critical application error, unknown application status: %s', application_status)

my_function()
print("printing details:")
print(enrollment_list)
