
import sys
import logging

from logging.handlers import SysLogHandler

LOG_SERVER_ADDR = '<putyourserverhere'
LOG_SERVER_PORT = 569 #defaulted to port 569 can be changed

logger = logging.getLogger('Manthis')

# LOCAL5 --> manthis.log
# LOCAL6 --> logserver.log
handler = SysLogHandler((LOG_SERVER_ADDR, LOG_SERVER_PORT), facility=SysLogHandler.LOG_LOCAL5)
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

argString = ' '.join(sys.argv)
logger.info("Test")
