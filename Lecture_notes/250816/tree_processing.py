from tree_def_class import *
from tree_def import *

'''
def bigs(t):
    
    >>> a = tree(1, [tree(4, [tree(4), tree(5)]), tree(3, [tree(0, [tree(2)])])])
    >>> bigs(a)
    4
    >>> b = tree(2, [tree(3, [tree(2, [tree(4), tree(1)])]), tree(1, [tree(2, [tree(1), tree(4)]), tree(3, [tree(1)])])])
    >>> bigs(b)
    5

    def f(a, x):
        if a.label > x:
            return 1 + sum(f(b, max(a.label, x)) for b in a.branches)
        else:
            return sum(f(b, max(a.label, x)) for b in a.branches)
    return f(t, t.label) + 1
    
    def f(a, x):
        if label(a) > x:
            return 1 + sum(f(b, label(a)) for b in branches(a))
        else:
            return sum(f(b, x) for b in branches(a))
    return f(t, label(t)) + 1
    '''

def bigs(t):
    '''
    >>> a = tree(1, [tree(4, [tree(4), tree(5)]), tree(3, [tree(0, [tree(2)])])])
    >>> bigs(a)
    4
    >>> b = tree(2, [tree(3, [tree(2, [tree(4), tree(1)])]), tree(1, [tree(2, [tree(1), tree(4)]), tree(3, [tree(1)])])])
    >>> bigs(b)
    5
    '''
    n = [0]
    def f(a, x):
        if label(a) > x:
            n[0] += 1
        
        for b in branches(a):
            f(b, max(label(a), x))
    f(t, label(t) - 1)
    return n[0]