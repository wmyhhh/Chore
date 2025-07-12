# a compound data object has an 'identity' in addtion to the pieces of which it is composed
# a list is still the 'same list' when we change its content
'''
>>> a = [1, 2]
>>> b = a
>>> a.append(3)
>>> a == b
True
>>> a
[1, 2, 3]
>>> b
[1, 2, 3]
>>> a = [1]
>>> b = [1]
>>> a.append(2)
>>> a == b
False
>>> a
[1, 2]
>>> b
[1]
'''

# identity vs equality
#  'is'    vs   '=='
'''
>>> a = [1]
>>> b = [1]
>>> a == b
True
>>> a is b
False
>>> c = b
>>> c.pop()
1
>>> c == b
True
>>> c is b
True
'''

# caution: mutable default argument
'''
>>> def f(s=[]):
...     s.append(3)
...     return len(s)
>>> f()
1
>>> f()
2
>>> f()
3
'''