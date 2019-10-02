#!/usr/bin/python
from Gen_CA import Secure

x = Secure('Config.yaml')
x.DumpKeyCertCsr()
