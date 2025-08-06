# TypeError, NameError, KeyError, RecursionError

def double(x):
    if type(x) == str:
        raise TypeError('wrong type')
    return x * 2

    '''
    >>> raise TypeError
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    TypeError
    >>> raise TypeError('very bad idea')
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    TypeError: very bad idea
    >>> double(4)
    8
    >>> double('4')
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "D:/Study/CS/UCB_CS61A/Lecture_notes/250730/exceptions.py", line 5, in double
        raise TypeError('wrong type')
    TypeError: wrong type
    >>>

    >>> hello
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    NameError: name 'hello' is not defined. Did you mean: 'help'?
    >>> {}['hello']
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    KeyError: 'hello'
    >>> def f():
    ...     f()
    ...
    >>> f()
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "<stdin>", line 2, in f
    File "<stdin>", line 2, in f
    File "<stdin>", line 2, in f
    [Previous line repeated 996 more times]
    RecursionError: maximum recursion depth exceeded
    >>> def func(x):
    ...     x *= 2
    ...
    >>> x = func(2)
    >>> x
    >>> def fun(x):
    ...     x *= 2
    ...     return x
    ...
    >>> x = fun(4)
    >>> x
    8
    '''

def invert(x):
    result = 1 / x
    print('Never printed if x is 0')
    return result

def invert_safe(x):
    try:
        return invert(x)
    except ZeroDivisionError as e:
        return str(e)
    

print('invert', invert(4))
print('invertsafe', invert_safe(4))
invert_safe(0)