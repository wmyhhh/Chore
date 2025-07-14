# iter(iterable)
# next(iterator)

'''
>>> s = [1, 2, 3]
>>> t = iter(s)
>>> next(t)
1
>>> next(t)
2
>>> k = iter(s)
>>> next(k)
1
>>> next(t)
3
>>> next(t)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

>>> s = [[1, 2], 3, 4, 5]
>>> next(s)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'list' object is not an iterator

>>> t = iter(s)
>>> list(t)
[[1, 2], 3, 4, 5]
>>> next(t)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration

>>> t = iter(s)
>>> next(t)
[1, 2]
>>> next(t)
3
>>> list(t)
[4, 5]
'''

# iter(iterable) -> iterator
# next(iterator)
# all iteratora are mutable
# case of dictionary
'''
>>> d = {'a': 1, 'b': 2, 'c': 3}
>>> x = iter(d.keys())
>>> next(x)
'a'
>>> next(x)
'b'
>>> y = iter(d.values())
>>> next(y)
1
>>> next(y)
2
>>> z = iter(d.items())
>>> next(z)
('a', 1)
>>> next(z)
('b', 2)
'''
# during iteration values bind to keys can be changed, but the size of dict can't

# iterable vs iterator
'''
>>> r = (1, 2, 3)
>>> for i in r:
...     print(i)
...
1
2
3
>>> for i in r:
...     print(i)
...
1
2
3
>>> k = iter(r)
>>> for i in k:
...     print(i)
...
1
2
3
>>> for i in k:
...     print(i)
...
'''