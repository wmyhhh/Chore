'''
Data abstraction
isolate two parts of program that use data:
how data are represented (as parts)
how data are manipulated (as units)

Example
rational(n,d) returns a rational number x <-- constructor
numer(x) returns the numerator of x <-- selector
denom(x) returns the denominator of x <-- selector
'''
from fractions import gcd

def rational(n,d):
    g = gcd(n,d)
    return [n // g, d // g]

def numer(x):
    return x[0]

def denom(x):
    return x[1]

def mul_ration(x,y):
    return rational(numer(x) * numer(y), denom(x) * denom(y))