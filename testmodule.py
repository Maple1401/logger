# Add these two lines in ALL MODULES
import logging
logger = logging.getLogger('global-log')

def exfunc():
	logger.info('Just a module doing module things')
	logger.debug('Debug msg behind the scenes')