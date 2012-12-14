
import os.path
import sys
import logging

from AdaptableSysLogHandler import AdaptableSysLogHandler
from logging.handlers import SysLogHandler #@UnresolvedImport
from logging.handlers import RotatingFileHandler #@UnresolvedImport

LOG_SERVER_ADDR = '<putyoursitenamehere'
LOG_SERVER_PORT = 569 #Default port can be altered if needed

def getDefaultLogger(name=None):
    logger = getLogger(name, [getLocalSyslogHandler(), getLogServerHandler()])
    return logger

def getLogger(name, handlers):
    logger = logging.getLogger(name) #@UndefinedVariable
    allHandlerClasses = [ h.__class__ for h in logger.handlers]
    for handler in handlers:
        if not handler.__class__ in allHandlerClasses:
            logger.addHandler(handler)
    return logger

def getLocalSyslogHandler():
    handler = AdaptableSysLogHandler()
    formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s') #@UndefinedVariable
    handler.setFormatter(formatter)
    return handler

def getLocalSyslogLogger(name=None):
    return getLogger(name, [getLocalSyslogHandler()])

def getLogServerHandler():
    handler = SysLogHandler((LOG_SERVER_ADDR, LOG_SERVER_PORT), facility=SysLogHandler.LOG_LOCAL6)
    formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s') #@UndefinedVariable
    handler.setFormatter(formatter)
    return handler

def getLogServerLogger(name=None):
    return getLogger(name, [getLogServerHandler()])

def getRotatingFileHandler(filename=None):
    if filename == None:
        if sys.platform == 'darwin':
            filename = os.path.expanduser('~/Library/Logs/Python/python.log')
        else:
            filename = '/var/local/log/python.log'
    handler = RotatingFileHandler(filename)
    formatter = logging.Formatter('%(asctime)s - %(name)s: %(levelname)s %(message)s') #@UndefinedVariable
    formatter.datefmt = "%d %b %Y %H:%M:%S"
    handler.setFormatter(formatter)
    return handler

def getRotatingFileLogger(name=None, filename=None):
    return getLogger(name, [getRotatingFileHandler()])

