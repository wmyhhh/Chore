# a built-in iterator function calculates the results lazily
# which means it only computes when it's called
# e.g. map, filter, reversed

'''
>>> def double(x):
...     print('**', x, '->', x*2, '**')
...     return 2 * x
...
>>> f = lambda x: x >= 10
>>> m = map(double, range(2,8))
>>> t = filter(f, m)
>>> next(t)
** 2 -> 4 **
** 3 -> 6 **
** 4 -> 8 **
** 5 -> 10 **
10
>>> next(t)
** 6 -> 12 **
12
>>> t = filter(f, m)
>>> next(t)           --> it continues iteration
** 7 -> 14 **
14
>>> m = map(double, range(2, 8))          --> this starts new iteration
>>> t = filter(f, m)
>>> next(t)
** 2 -> 4 **
** 3 -> 6 **
** 4 -> 8 **
** 5 -> 10 **
10
>>> t
<filter object at 0x000002BA7E2EFC70>
>>> next(t)
** 6 -> 12 **
12
>>> t
<filter object at 0x000002BA7E2EFC70>

>>> list(filter(f, map(double, range(2,8))))    --> but list() get it out all at once
** 2 -> 4 **
** 3 -> 6 **
** 4 -> 8 **
** 5 -> 10 **
** 6 -> 12 **
** 7 -> 14 **
[10, 12, 14]
'''

# reversed() can be tricky sometimes
'''
>>> s = [1, 2, 3, 2, 1]
>>> t = reversed(s)
>>> t
<list_reverseiterator object at 0x000002BA7E2EF100>
>>> t == s
False
>>> list(t) == s
True
'''

# zip!
'''
>>> list(zip([1, 3, 5], [2, 4, 6]))
[(1, 2), (3, 4), (5, 6)]

>>> list(zip([1, 2, 3, 4], [11, 33]))
[(1, 11), (2, 33)]

>>> list(zip([1, 2], [3, 4], [5, 6]))
[(1, 3, 5), (2, 4, 6)]
>>>'''

def palindrome1(x):
    return list(x) == list(reversed(x))

def palindrome2(x):
    return all(a == b for a, b in zip(x, reversed(x)))

'''
>>> [a == b for a, b in zip(s, reversed(s))]
[True, True, True, True, True]
>>> all([a == b for a, b in zip(s, reversed(s))])
True
'''