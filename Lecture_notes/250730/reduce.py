from operator import add, mul, truediv

def divide_all(n, ds):
    try:
        return reduce_iter(truediv, ds, n)
    except ZeroDivisionError:
        return 0

def reduce_iter(f, s, initial):
    '''
    >>> reduce(mul, [2, 4, 8], 1)
    64
    >>> reduce(add, [1, 2, 3, 4], 0)
    10
    '''
    for i in s:
        initial = f(initial, i) # pay attention to the order!
    return initial

def reduce_recur(f, s, initial):
    '''
    >>> reduce(mul, [2, 4, 8], 1)
    64
    >>> reduce(add, [1, 2, 3, 4], 0)
    10
    '''
    if not s:
        return initial
    else:
        first, rest = s[0], s[1:]
        return reduce_recur(f, rest, f(first, initial))