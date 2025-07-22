from linked_list import *
def range_link(start, end):
    if start >= end:
        return Link.empty
    else:
        return Link(start, range_link(start + 1, end))
    
def map_link(f, s):
    if s is Link.empty:
        return s
    else:
        return Link(f(s.first), map_link(f, s.rest))
    
def filter_link(f, s):
    if s is Link.empty:
        return s
    filtered = filter_link(f, s.rest)
    if f(s.first):
        return Link(s.first, filtered)
    else:
        return filtered
    
'''
>>> t = filter_link(lambda x: x % 2 == 0, range_link(1,10))
>>> k = map_link(lambda x: x * x, t)
>>> k
Link(4, Link(16, Link(36, Link(64))))'''

def add(s, v):
# this won't change s
    '''
    if s is Link.empty:
        return Link(v)
    elif v < s.first:
        return Link(v, s)
    elif v == s.first:
        return s
    else:
        return Link(s.first, add(s.rest, v))
    '''
    if v < s.first:
        s.first, s.rest = v, Link(s.first, s.rest) # not s
    elif v > s.first and s.rest is Link.empty:
        s.rest = Link(v)
    elif v > s.first:
        add(s.rest, v)
    return s
        
        