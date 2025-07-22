def count_frames(f):
    def counted(n):
        counted.open_count += 1
        if counted.open_count > counted.max_count:
            counted.max_count = counted.open_count
        result = f(n)
        counted.open_count -= 1
        return result
    counted.open_count = 0
    counted.max_count = 0
    return counted

def fib(n):
    if n == 1 or n == 0:
        return n
    else:
        return fib(n - 2) + fib(n - 1)
'''
>>> fib = count_frames(fib)
>>> a = fib
>>> b = fib
>>> a(20)
6765
>>> a.max_count
20
>>> b(30)
832040
>>> b.max_count
30'''
