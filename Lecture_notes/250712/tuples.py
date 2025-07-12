'''
>>> (2, 3, 4)
(2, 3, 4)
>>> 2, 3, 4,
(2, 3, 4)
>>> 2,
(2,)
>>> ()
()
>>> (2, 4) + (2, 5)
(2, 4, 2, 5)
>>> 3 in (1, 2, 3)

>>> {(1, 2):8}
{(1, 2): 8}
>>> {[1, 2]:8}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> {(1, [2]):8}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
'''

# tuples are immutable sequences
# immutable values are protected from mutation

# immutable values can still change when it contains a mutable value
'''
>>> t = ([1, 2], 3)
>>> t[0] = [1]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> t[0][0] = 3    #can change the element in the list
>>> t
([3, 2], 3)
'''