from ucb import trace

def my_trace(f):
    def g(x):
        print("calling", f, "on", x)
        return f(x)
    return g

@trace
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 2) + fib(n - 1)
    
@trace
def fib_iter(n):
    pre, cur, k = 1, 0, 1
    while k <= n:
        pre, cur = cur, pre + cur
        k += 1
    return cur