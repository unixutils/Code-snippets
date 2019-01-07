#!/usr/bin/python
import requests
import re

payload = {'s': 'python'}
req = requests.get('https://unixutils.com/', params=payload)

print "URL:",req.url
print "HTTP Status code:",req.status_code
result = re.search('<title>(.*)</title>', req.content)
print "Title of the visited URL:",result.group(1)

