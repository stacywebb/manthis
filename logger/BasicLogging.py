
import sys
import logging

from logging.handlers import SysLogHandler

LOG_SERVER_ADDR = '<putyoursitenameher>'
LOG_SERVER_PORT = 569 #default can be customized

logger = logging.getLogger('Manthis')

# LOCAL5 --> manthis.log
# LOCAL6 --> logserver.log
handler = SysLogHandler((LOG_SERVER_ADDR, LOG_SERVER_PORT), facility=SysLogHandler.LOG_LOCAL5)
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def log(msg):
    logger.info(msg)
    
if __name__ == '__main__':
    log("log5.log client initialized")