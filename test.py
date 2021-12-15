import pickle
import os
from display_by_person import load_pickle


data = load_pickle("embeddings.pickle")

for dictionary in data:
    print(dictionary['path'])