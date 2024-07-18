import pickle
import sys

with open(sys.argv[1], 'wb') as f:
    pickle.dump([], f)
