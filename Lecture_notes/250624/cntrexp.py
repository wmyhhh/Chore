'''
short circuiting 
and & or
'''
from math import sqrt

def big_sqrt(x):
    return x>0 and sqrt(x)>10

def reasonable(x):
    return x == 0 or 1/x != 0
