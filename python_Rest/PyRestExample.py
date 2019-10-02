#!/usr/bin/python
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
scriptdir = os.path.dirname(here)
sys.path.append(os.path.join(here, 'lib'))

from RestOperations import RestOperations
rest = RestOperations('https://url.com/public-api/', authType = 'token', token = 'gXE1CWifeADQyCK7TfuxKuns1_GjFthFT2sB')
print(rest.SendGetReq().text)
