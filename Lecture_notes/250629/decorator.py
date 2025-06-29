def trace1(fn):
    def traced(x):
        print('calling',fn,'evaluate on',x)
        return fn(x)
    return traced

@trace1
def square(x):
    return x * x

@trace1
def sum_square(n):
    k, tot = 1, n
    while k <= n:
        tot, k = tot + square(k), k+1
    return tot



