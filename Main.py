__author__ = 'matt'
#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import gevent.monkey; gevent.monkey.patch_all()
import RESTInterface
import logging
import logging.handlers
import bottle
import WebInterface
import Polling
import Scheduler
import HomerHelper
from gevent import monkey,sleep,joinall,spawn


logging_level = 'DEBUG'

log_type = ('logging.'+logging_level)
logging.basicConfig(format='%(asctime)s %(name)s-%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='/var/log/HOMEr.log',level=logging.DEBUG)
logging.handlers.TimedRotatingFileHandler(filename='/var/log/HOMEr.log', when='midnight',backupCount=7, encoding=None, delay=False, utc=False)
logging.info('HOMEr service started')

def endprog():
    logging.info('HOMEr service stopping')


bottleApp = bottle.default_app()
bottleApp.merge(RESTInterface.RESTApp)
bottleApp.merge(WebInterface.WebApp)

########################################################################
#gevent.spawn(Polling.HuePoll())
Polling.PollingStart()
bottleApp.run(reloader=True, host='0.0.0.0', port=8081, debug=True, server='gevent')