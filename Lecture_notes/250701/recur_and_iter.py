# recursion vs iteration

def fact_iter(n):
    i,tot = 1, 1
    while i <= n:
        tot *= i
        i += 1
    return tot

def fact_recur(n):
    if n == 0:
        return 1
    else:
        return n * fact_recur(n-1)
    
    
import timeit

print("Iteration:", timeit.timeit("fact_iter(500)", globals=globals(), number=1000))
print("Recursion:", timeit.timeit("fact_recur(500)", globals=globals(), number=1000))

'''
Iteration: 0.10345669998787344
Recursion: 0.13409509998746216
'''