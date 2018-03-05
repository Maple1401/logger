# -------------------------------------------------#
# Application: Logger Example (with purging)
# Author: Phill Johntony
# Date: 2018-03-05
# -------------------------------------------------#

import logging   # Logging library
import os        # Environment library
import traceback # Error handling
import datetime  # Date and Time
import time      # For log purging

import testmodule

def init_logger():
	try:
		# Log File Variables
		log_file_dir = 'log'
		log_file_dir = os.path.join(os.getcwd(), log_file_dir)
		log_file_name = 'example'
		log_file_ext = '.log'
		log_file_date = datetime.datetime.now().strftime("%Y%m%d")
		log_file_time = datetime.datetime.now().strftime("%H%M%S")
		log_file_fullname = (log_file_name + '-' + log_file_date + '-' + log_file_time + log_file_ext)
		log_file_actual = os.path.join(log_file_dir, log_file_fullname)

		# Create Log File directory if it does not exist
		if not os.path.exists(log_file_dir):
			os.mkdir(log_file_dir)

		# Global log FILE settings
		log_file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s -> %(message)s')
		log_file_handler = logging.FileHandler(log_file_actual)
		log_file_handler.setFormatter(log_file_formatter)

		# Global log CONSOLE settings
		log_console_formatter = logging.Formatter('%(asctime)s - %(message)s')
		log_console_handler = logging.StreamHandler()
		log_console_handler.setLevel(logging.INFO)
		log_console_handler.setFormatter(log_console_formatter)

		# Adds configurations to global log
		logger.setLevel(logging.DEBUG)
		logger.addHandler(log_file_handler)
		logger.addHandler(log_console_handler)

		# All is done, ready to accept logs
		logger.debug('Global Log initiated and configured')

		logger_purge(log_file_dir, log_file_ext)

	except IOError as e:
		errOut = "** ERROR: Unable to create or open log file %s" % log_file_name
		if e.errno is 2:
			errOut += "- No such directory **"
		elif e.errno is 13:
			errOut += " - Permission Denied **"
		elif e.errno is 24:
			errOut += " - Too many open files **"
		else:
			errOut += " - Unhandled Exception-> %s **" % str(e)
			sys.stderr.write(errOut + "\n")
			traceback.print_exc()

	except Exception:
		traceback.print_exc()

def logger_purge(log_file_dir, log_file_ext):
	try:
		# Purge old log files if set in config file
		logger.debug('Starting log purge check')
		retention_days = 1
		logger.debug('retention_days = ' + str(retention_days))
		if int(retention_days) > 0:
			retenion_sec = int(retention_days)*86400 # Convert days to seconds
			now = time.time()
			logger.debug('retenion_sec = ' + str(retenion_sec))
			logger.debug('now = ' + str(now))
			logger.debug('retenion_sec - now = ' + str(now - retenion_sec))
			for file in os.listdir(log_file_dir):
				logger.debug('Inspecting file: ' + file)
				# Only check for log files
				if file.endswith(log_file_ext):
					# logger.debug('Confirmed file ends with: ' + log_file_ext)
					filepath = os.path.join(log_file_dir, file)
					modified = os.stat(filepath).st_mtime
					logger.debug('File date modified is: ' + str(modified))
					if modified < now - retenion_sec:
						logger.debug('File date modified is past retention_days!')
						if os.path.isfile(filepath):
							os.remove(filepath)
							logger.debug(file + ' deleted!')

	except Exception:
		traceback.print_exc()

# -------------------------------------------------#

# Add this line in ALL MODULES
logger = logging.getLogger('global-log')

# Logger only needs initiated in the main script
init_logger()

# In this example the init calls logger_purge()
# But that can be moved to be run after reading a config file so the retenion days can be stored there.

logger.info('Starting script info msg')
logger.debug('Secret debug msg for the dev')

testmodule.exfunc()

logger.info('All done')