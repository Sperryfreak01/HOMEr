__author__ = 'matt'
#!/usr/bin/python
# -*- coding: utf-8 -*-

import RESTInterface
import logging
import logging.handlers
from bottle import *

logging_level = 'DEBUG'

log_type = ('logging.'+logging_level)
logging.basicConfig(format='%(asctime)s %(name)s-%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='/var/log/HOMEr.log',level=logging.DEBUG)
logging.handlers.TimedRotatingFileHandler(filename='/var/log/HOMEr.log', when='midnight',backupCount=7, encoding=None, delay=False, utc=False)
logging.info('HOMEr service started')

def endprog():
    logging.info('HOMEr service stopping')


########################################################################
run(reloader=True, host='0.0.0.0', port=8081, debug=True)


