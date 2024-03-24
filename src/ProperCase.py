
#######################################################################################################################
####################################################### IMPORTS #######################################################
#######################################################################################################################

import requests
from googlesearch import search, get_random_user_agent # This package is onfusingly named simply "google" when
	# installing via PIP (see https://github.com/MarioVilas/googlesearch)
import re
import time
from DataObjects import load_obj, save_obj
import sys
import traceback
from bs4 import BeautifulSoup
from StandardLogging import Logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

#######################################################################################################################
################################################### GET_PROPERCASE ####################################################
#######################################################################################################################

def get(url: str, retry_get_upon_error=False, silent=False):

	def single_get_attempt(url, silent=False):

		# Get webpage content for this url
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
		r = requests.get(url, headers=headers, timeout=5)

		# Raise exception if status code is not 200
		r.raise_for_status()

		# Parse html
		soup = BeautifulSoup(r.content, 'html.parser')

		# Remove hyperlinks
		soup.a.decompose()

		# Extract text
		text = soup.get_text()
		return text

	if retry_get_upon_error == True:
		try:
			return single_get_attempt(url)
		except:
			try:
				Logging.critical("\tFirst error trying to retrieve: " + str(url), silent=silent)
				time.sleep(1.5)
				return single_get_attempt(url)
			except:
				try:
					Logging.critical("\tGiving up after second error trying to retrieve: " + str(url), silent=silent)
					time.sleep(2.5)
					return single_get_attempt(url)
				except:
					return None
	elif retry_get_upon_error == False:
		try:
			return single_get_attempt(url)
		except:
			Logging(silent=silent).debug("\tUnable to retrieve: " + str(url))
			return None
	else:
		pass

def make_requests(urls: list[str], retry_get_upon_error=False, silent=False):
	with tqdm(total=len(urls)) as pbar:
		with ThreadPoolExecutor(max_workers=5) as executor:
			futures = [executor.submit(get, url, retry_get_upon_error=retry_get_upon_error, silent=silent) for url in
			           urls]
			for future in as_completed(futures):
				pbar.update(1)
				yield future.result()
def Get_ProperCase(keyword: str, googlesearch_depth=50, googlesearch_pause=0.5, retry_get_upon_error=False,
                   silent=False, multithread=True):

	Logging(silent=silent).critical("")
	Logging(silent=silent).critical("\tDetermining proper case for " + keyword + "...")

	# Load and check capitalization_database (if any already exists)
	try:
		cap_db = load_obj(sys.path[0] + '/capitalization_database')
	except:
		Logging(silent=silent).critical("\tUnable to locate existing capitalization_database so we\'ll start from "
		                           "scratch...")
		cap_db = {}
	try:
		propercase_keyword = cap_db[keyword]
		if propercase_keyword != propercase_keyword.lower():
			check_case = False
			Logging(silent=silent).critical("\t\tFound keyword in capitalization database!")
			Logging(silent=silent).critical("\t\tProper capitalization of \"" + keyword + "\" is \""
			                                + propercase_keyword + "\"")
		else:
			check_case = True
	except:
		check_case = True

	# Check Google search results if keyword not in capitalization_database
	if check_case == True:
		results = []
		for url in search(keyword, tld='com', lang='en', num=googlesearch_depth, start=0,stop=googlesearch_depth,
		                  pause=googlesearch_pause, user_agent=get_random_user_agent()):
			results.append(url)
		'''
		### url contents ###
		keyword : query string that we want to search for.
		tld : tld stands for top level domain which means we want to search our result on google.com or google.in or  
			some other domain.
		lang : lang stands for language.
		num : Number of results per page.
		start : First result to retrieve.
		stop : Last result to retrieve. Use None to keep searching forever.
		pause : Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping  
			significant lapse will make your program slow but its safe and better option.
		Return : Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop 
			forever.
		'''
		capitalization_occurrence_tracker = {}
		if multithread == True:
			outputs = []
			for output in make_requests(results, retry_get_upon_error=retry_get_upon_error, silent=silent):
				outputs.append(output)
			for output in outputs:
				try:
					matches = re.findall('(?i)' + re.escape(keyword), output)
					for match in matches:
						if match == None:
							pass
						else:
							try:
								if match not in capitalization_occurrence_tracker:
									capitalization_occurrence_tracker[match] = 1
								elif match in capitalization_occurrence_tracker:
									capitalization_occurrence_tracker[match] = (capitalization_occurrence_tracker[match]
									                                            + 1)
							except:
								pass
				except:
					pass
		elif multithread == False:
			for url in tqdm(results):
				try:
					text = get(url, retry_get_upon_error=retry_get_upon_error)
					matches = re.findall('(?i)' + keyword, text)
					for match in matches:
						if match == None:
							pass
						else:
							try:
								if match not in capitalization_occurrence_tracker:
									capitalization_occurrence_tracker[match] = 1
								elif match in capitalization_occurrence_tracker:
									capitalization_occurrence_tracker[match] = (capitalization_occurrence_tracker[match]
									                                            + 1)
							except:
								pass
				except:
					pass
		else:
			Logging(silent=silent).critical("Unexpected multithread parameter:  " + str(multithread))
		if bool(capitalization_occurrence_tracker) == False:
			Logging(silent=silent).critical("\tUnable to locate examples of \"" + keyword
			                                + "\" in Google search results...")
			return None
		elif bool(capitalization_occurrence_tracker) == True:
			most_frequent_capitalization = max(capitalization_occurrence_tracker,
			                                   key=capitalization_occurrence_tracker.get)
			Logging(silent=silent).critical("\t\tIdentified the following capitalizations:")
			sorted_keys = sorted(capitalization_occurrence_tracker, key=capitalization_occurrence_tracker.get,
			                     reverse=True)
			for key in sorted_keys:
				Logging(silent=silent).critical("\t\t\t" + str(key) + ":  "
				                                + str(capitalization_occurrence_tracker[key]) + " occurences",)
			if most_frequent_capitalization == keyword.title():
				try:
					title_case_count = capitalization_occurrence_tracker[keyword.title()]
					try:
						lower_case_count = capitalization_occurrence_tracker[keyword.lower()]
					except:
						lower_case_count = 0
					caps_ratio = title_case_count / (title_case_count + lower_case_count)
					if caps_ratio > 0.65:
						propercase_keyword = keyword.title()
					else:
						propercase_keyword = keyword.lower()
				except Exception as e:
					Logging(silent=silent).critical("Uh oh! Ran into error while determining capitaliztion:  " + str(e))
					traceback.print_exc()
			else:
				propercase_keyword = most_frequent_capitalization
			Logging(silent=silent).critical("\t\tProper capitalization of \"" + keyword + "\" is \""
			                                + propercase_keyword + "\"")
			cap_db[keyword] = propercase_keyword
			save_obj(cap_db, sys.path[0] + '/capitalization_database')

	return propercase_keyword

if __name__ == "__main__":

	### EXPLANATORY EXAMPLES AND COMMENTS ###

	# Example 1 (Using Keyword Already in Capitalization Database)
	keyword = "mcdonald\'s"
	PC_keyword = Get_ProperCase(                            # Get_ProperCase's output is a string (keyword with proper capitalization)
								keyword,                    # Str: keyword of which the user wants to determine the proper capitalization)
								googlesearch_depth=50,      # Int: Number of Google search results to review (if keyword # not in capitalization database); default is 50
								googlesearch_pause=0.5,     # Float/Int: Number of seconds between Google search queries (if necessary); default is 0.5
								retry_get_upon_error=False, # Bool: Whether to retry URL if first attempt results in error; default is False (no)
								silent=False,               # Bool: Whether to create logs and print important log messages to standard out; default is False (not silent--creates logs and prints important log messages)
								multithread=True            # Bool: Whether to use multithreading for obtaining text of URLs; default is True (yes)
								)

	# Example 2 (Using Keyword Not Found in Capitalization Database)
	keyword = "deadmau5"
	PC_keyword = Get_ProperCase(                            # Get_ProperCase's output is a string (keyword with proper capitalization)
								keyword,                    # Str: keyword of which the user wants to determine the proper capitalization)
								googlesearch_depth=50,      # Int: Number of Google search results to review (if keyword # not in capitalization database); default is 50
								googlesearch_pause=0.5,     # Float/Int: Number of seconds between Google search queries (if necessary); default is 0.5
								retry_get_upon_error=False, # Bool: Whether to retry URL if first attempt results in error; default is False (no)
								silent=False,               # Bool: Whether to create logs and print important log messages to standard out; default is False (not silent--creates logs and prints important log messages)
								multithread=True            # Bool: Whether to use multithreading for obtaining text of URLs; default is True (yes)
								)









