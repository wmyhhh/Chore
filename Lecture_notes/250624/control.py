from math import sqrt
'''
def real_sqrt(x):
    if x>=0:
        return sqrt(x)
    else:
        return 0
'''
def if_(a,b,c):
    if a:
        return b
    else:
        return c
    
def real_sqrt(x):
    return if_(x>=0,sqrt(x),0)