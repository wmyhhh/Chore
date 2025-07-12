from tree_rw import *

def count_paths(t,total):
    if label(t) == total:
        found = 1
        
    else:
        found = 0
    return found + sum(count_paths(b, total - label(t)) for b in branches)