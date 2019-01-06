#!/usr/bin/python
import logging
import sys

logging.basicConfig(filename='application.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

employee_name = sys.argv[1]
employee_age  = int(sys.argv[2])
application_status = sys.argv[3]
enrollment_list = []


if application_status == "failed":
   print "Enrollment failed since application status is failed"
   logging.error('Enrollment failed for: %s', employee_name)
elif employee_age > 55 and application_status == 'passed':
   enrollment_list.append(employee_name+':'+str(employee_age)+':'+application_status)
   logging.warn('Enrollment successful for: %s', employee_name)
   logging.warn('age is above threshold')
elif employee_age < 55 and application_status == 'passed':
   enrollment_list.append(employee_name+':'+str(employee_age)+':'+application_status)
   logging.info('Enrollment successful for: %s', employee_name)
else:
   print "Critical application error, unknown application status"
   logging.critical('Enrollment failed for: %s', employee_name)
   logging.critical('Critical application error, unknown application status: %s', application_status)

print("printing details:")
print(enrollment_list)

