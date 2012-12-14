import sys
import logging.handlers

class AdaptableSysLogHandler(logging.handlers.SysLogHandler):

    def __init__(self):
        if sys.platform == 'darwin':
            address = '/var/run/syslog'
        else:
            address = '/dev/log'
        logging.handlers.SysLogHandler.__init__(self, address)
        
    
        
