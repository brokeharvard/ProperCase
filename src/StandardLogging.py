#######################################################################################################################
####################################################### IMPORTS #######################################################
#######################################################################################################################

# Logging Modules
import os
import sys
import logging
import datetime as dt
import errno

#######################################################################################################################
################################################ STANDARD LOGGING SETUP ###############################################
#######################################################################################################################

# Make logs subfolder if doesn't already exist
if not os.path.exists(os.path.dirname('Logs')):
	try:
		os.makedirs('Logs')
	except OSError as exc:  # Guard against race condition
		if exc.errno != errno.EEXIST:
			raise

# Determine log file names
filename = os.path.basename(sys.argv[0])
start_date = log_filename = dt.datetime.now().strftime('%m-%d-%Y')
log_filename = 'Logs/' + dt.datetime.now().strftime(filename + '_%m-%d-%Y.txt')
debug_log_filename = 'Logs/' + dt.datetime.now().strftime(filename + '_%m-%d-%Y.debug.txt')

# Set up logging to file for DEBUG level or higher
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  ==  %(levelname)-8s  ==  %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=debug_log_filename,
                    # filemode='w' # This would overwrite any logfile with same name (e.g., if ran twice
                    # in single day).
                    # Default is 'a'.
                    )

# Define a file handler which logs only messages with CRITICAL level or higher
fh = logging.FileHandler(log_filename)
fh.setLevel(logging.CRITICAL)

# Set a format for fh log use
formatter = logging.Formatter('%(asctime)s  ==  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Tell the handler to use this format
fh.setFormatter(formatter)

# add the handler to the logger
logging.getLogger('').addHandler(fh)

# Define a handler which writes WARNING messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.WARNING)

# Set a format for console use
formatter = logging.Formatter('%(asctime)s  ==  %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Tell the handler to use this format
console.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger('').addHandler(console)

'''
### LOGGING NOTES ###

	- For debug logging (won't show up in console), use:  logging.debug('')
	- For logging that will also show up in console, use:  logging.critical('')

'''

class Logging():
	def __init__(self, silent=False):
		self.silent = silent
		if silent == False:
			self.logging = logging
		elif silent == True:
			pass
		else:
			print("Logging class received unexpected \"silent\" parameter:  " + str(silent))
	def emergency(self, text):
		if self.silent == False:
			self.logging.emergency(text)
		else:
			pass
	def alert(self, text):
		if self.silent == False:
			self.logging.alert(text)
		else:
			pass
	def critical(self, text):
		if self.silent == False:
			self.logging.critical(text)
		else:
			pass
	def error(self, text):
		if self.silent == False:
			self.logging.error(text)
		else:
			pass
	def warning(self, text):
		if self.silent == False:
			self.logging.warning(text)
		else:
			pass
	def informational(self, text):
		if self.silent == False:
			self.logging.informational(text)
		else:
			pass
	def debug(self, text):
		if self.silent == False:
			self.logging.debug(text)
		else:
			pass
