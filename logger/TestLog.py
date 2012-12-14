
import logging

from logger import LoggerFactory


logger = LoggerFactory.getDefaultLogger()
logger = LoggerFactory.getDefaultLogger()
logger.setLevel(logging.INFO) #@UndefinedVariable
logger.info('Here is some information for you')
logger.warning('Oh Hai, here is a warning.')



