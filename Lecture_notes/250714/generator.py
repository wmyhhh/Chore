# generator is a type of iterator
# a generator is returned from a generator function
# a generator function yields values instead of returning them
# a normal function returns once, a generator function can yield multiple times
# when a generator function is called it returns a generator that iterate over its yields
'''
>>> t = plus_minus(3)
>>> t
<generator object plus_minus at 0x0000028A77934C40>
>>> next(t)
3
>>> next(t)
-3'''

'''
>>> def even(start, end):
...     x = start + (start % 2)
...     while x <= end:
...             yield x
...             x += 2
...
>>> t = even(1, 10)
>>> next(t)
2
>>> list(t)
[4, 6, 8, 10]
'''

# yield from: yield all the values from an iterator or iterable
'''
>>> def combine(a, b):
...     yield from a
...     yield from b
...
>>> combine([1, 2], [3, 4])
<generator object combine at 0x0000028A779FE740>
>>> list(combine([1, 2], [3, 4]))
[1, 2, 3, 4]
>>>

>>> def countdown(k):
...     if k > 0:
...             yield k
...             yield from countdown(k - 1)
...     else:
...             yield 'blast off'
...
>>> list(countdown(3))
[3, 2, 1, 'blast off']

>>> for i in countdown(5):
...     print(i)
...
5
4
3
2
1
blast off
>>>

>>> def prefixes(x):
...     if x:
...             yield from prefixes(x[:-1])
...             yield x
...
>>> list(prefixes('hellooo'))
['h', 'he', 'hel', 'hell', 'hello', 'helloo', 'hellooo']

>>> def substrings(x):
...     if x:
...             yield from prefixes(x)
...             yield from substrings(x[1:])
...
>>> list(substrings('top1'))
['t', 'to', 'top', 'top1', 'o', 'op', 'op1', 'p', 'p1', '1']
>>>'''
