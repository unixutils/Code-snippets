#!/usr/bin/python
import requests

req = requests.get('https://unixutils.com/')  
print "URL:",req.url
print "HEADERS:",req.headers



