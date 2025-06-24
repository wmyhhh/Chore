from operator import add, mul, truediv, floordiv, mod
#print(truediv(23,5), floordiv(23,5),mod(23,5))
def div(n,d):
    '''
    >>> q,r = div(23,5)
    >>> q
    4
    >>> r
    3

    '''
    return floordiv(n,d), mod(n,d)

q,r = div(231,11)
#print(q,r)

'''
python -i miscellaneous.py
python -m doctest -v miscellaneous.py
'''