'''
seperate with layers of abstraction'''

# constructors and selectors
from math import gcd

def pre_rational(n,d):
    g = gcd(n,d)
    return [n // g, d // g]

def pre_numer(x):
    return x[0]

def pre_denom(x):
    return x[1]

def rational(n,d):
    def select(name):
        if name == 'n':
            return n
        elif name == 'd':
            return d
    return select

def numer(x):
    return x('n')

def denom(x):
    return x('d')

# rational arithmetic
def mul_rational(x, y):
    return rational(numer(x) * numer(y), denom(x) * denom(y))

def add_rational(x, y):
    return rational(numer(x) * denom (y) + numer(y) * denom(x),
                    denom(x) * denom(y))

def rational_equal(x,y):
    return denom(x) * numer(y) == denom(y) * numer(x)

def print_rational(x):
    print(numer(x), '/', denom(x))