# ProperCase
 
### What is ProperCase?
 ProperCase determines the proper capitalization of a given word or phrase (e.g., "McDonald's") by:  (1) checking a 
 database of proper nouns for the proper capitalization of the given word or phrase; and (2) solely if the given 
 word or phrase is not in the database, reviewing the capitalization of the word or phrase in top Google search 
 results (in which case the proper capitalization of the word or phrase is added to the database).

### How do you use ProperCase?
 

ProperCase's principal function is Get_ProperCase, which takes a string (the word or phrase of which the user wants 
to determine the proper capitalization) as its only mandatory parameter and outputs that string with its proper 
capitalization.  See below for explanatory examples and comments, including with respect to Get_ProperCase's several 
optional parameters.

#### Example 1 (Using Keyword Already in Capitalization Database)

###### Code:
```python
from ProperCase import Get_ProperCase

keyword = "mcdonald\'s"
PC_keyword = Get_ProperCase(                            # Get_ProperCase's output is a string (keyword with proper capitalization)
                            keyword,                    # Str: keyword of which the user wants to determine the proper capitalization)
                            googlesearch_depth=50,      # Int: Number of Google search results to review (if keyword not in capitalization database); default is 50
                            googlesearch_pause=0.5,     # Float/Int: Number of seconds between Google search queries (if necessary); default is 0.5                
                            retry_get_upon_error=False, # Bool: Whether to retry URL if first attempt results in error; default is False (no)
                            silent=False,               # Bool: Whether to create logs and print important log messages to standard out; default is False (not silent--creates logs and prints important log messages)
                            multithread=True            # Bool: Whether to use multithreading for obtaining text of URLs; default is True (yes)
                            )
```
###### Output:
```
03/24/2024 05:00:00 PM  ==  	Determining proper case for mcdonald's...
03/24/2024 05:00:00 PM  ==  		Found keyword in capitalization database!
03/24/2024 05:00:00 PM  ==  		Proper capitalization of "mcdonald's" is "McDonald's"
```

#### Example 2 (Using Keyword Not Found in Capitalization Database)

###### Code:
```python
from ProperCase import Get_ProperCase

keyword = "deadmau5"
PC_keyword = Get_ProperCase(                            # Get_ProperCase's output is a string (keyword with proper capitalization)
                            keyword,                    # Str: keyword of which the user wants to determine the proper capitalization)
                            googlesearch_depth=50,      # Int: Number of Google search results to review (if keyword not in capitalization database); default is 50
                            googlesearch_pause=0.5,     # Float/Int: Number of seconds between Google search queries (if necessary); default is 0.5                
                            retry_get_upon_error=False, # Bool: Whether to retry URL if first attempt results in error; default is False (no)
                            silent=False,               # Bool: Whether to create logs and print important log messages to standard out; default is False (not silent--creates logs and prints important log messages)
                            multithread=True            # Bool: Whether to use multithreading for obtaining text of URLs; default is True (yes)
                            )
```
###### Output:
```
03/24/2024 05:02:50 PM  ==  	Determining proper case for deadmau5...
100%|██████████| 50/50 [00:06<00:00,  7.90it/s]
03/24/2024 05:02:59 PM  ==  		Identified the following capitalizations:
03/24/2024 05:02:59 PM  ==  			deadmau5:  452 occurences
03/24/2024 05:02:59 PM  ==  			Deadmau5:  291 occurences
03/24/2024 05:02:59 PM  ==  			DEADMAU5:  9 occurences
03/24/2024 05:02:59 PM  ==  			DeadMau5:  3 occurences
03/24/2024 05:02:59 PM  ==  		Proper capitalization of "deadmau5" is "deadmau5"
```