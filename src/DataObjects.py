import os
import pickle

## For saving dictionary to file
def save_obj(obj, name): # Name should not include extension
    filename = (name + '.pkl')
    try:
        os.makedirs(os.path.dirname(name), exist_ok=True)   # This requires Python 3
    except:
        pass
    with open(filename, 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
            #   HIGHEST_PROTOCOL is a binary format, which could not be always
            #   convenient, but is good for performance. Protocol 0 is a text
            #   format.

## For loading dictionary from file
def load_obj(name): # Name should not include extension
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
