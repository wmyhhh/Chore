# linear time
# doubling the input doubles the time
# 1024x input takes 1024x as much time
def exp(x, n):
    if x == 0:
        return 1
    else:
        return x * exp(x, n - 1)

def square(x):
    return x * x
    
# logarithmic time
# doubling the input increases the time by a constant C
# 1024x input increases the time by only 10 times C
def fast_exp(x, n):
    if n == 0:
        return 1
    elif x % 2 == 0:
        return square(fast_exp(x, n // 2))
    else:
        return x * fast_exp(x, n - 1)
    
# draw the graph