# in python all object produce two string representation
# str -> eligible to human
# repr -> eligible to python interpreter


# the repr function returns a python expression that evaluate to an equal object
# eval(repr(object)) == object

'''
>>> 12e12
12000000000000.0
>>> print(repr(12e12))
12000000000000.0
>>> print(12e12)
12000000000000.0
>>> repr(12e12)
'12000000000000.0'
>>> repr(min(13,15))
'13'
>>> repr(min)
'<built-in function min>
'''

# the result of calling str on the value of an expression is what python prints using the print function
'''
>>> from fractions import Fraction
>>> half =  Fraction(1,2)
>>> repr(half)
'Fraction(1, 2)'
>>> str(half)
'1/2'
>>> print(half)
1/2
>>> print(str(half))
1/2
>>> print(repr(half))
Fraction(1, 2)
>>> eval(str(half))
0.5
>>> eval(repr(half))
Fraction(1, 2)
'''

'''
>>> s = 'hello world'
>>> str(s)
'hello world'
>>> repr(s)
"'hello world'"
>>> print(str(s))
hello world
>>> print(s)
hello world
>>> print(repr(s))
'hello world'
>>> eval(str(s))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1
    hello world
          ^^^^^
SyntaxError: invalid syntax
>>> eval(s)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1
    hello world
          ^^^^^
SyntaxError: invalid syntax
>>> eval(repr(s))
'hello world'
>>> repr(repr(repr(s)))
'\'"\\\'hello world\\\'"\''
>>> eval(eval(eval(repr(repr(repr(s))))))
'hello world'
>>>
'''