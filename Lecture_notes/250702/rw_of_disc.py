def swipe(n):
    if n < 10:
        print(n)
    else:
        print(n % 10)
        swipe(n // 10) # without return here !!
        print(n % 10)

def skip_fact(n):
    if n <= 2:
        return n
    else:
        return n * skip_fact(n - 2)
    
def is_prime(n):
    if n < 2:
        return False
    def f(i):
        if i * i > n:
            return True
        elif n % i == 0:
            return False
        else:
            return f(i + 1)
    return f(2)

def hailstone(n):
    print(n)
    if n % 2 == 0:
        return even(n)
    else:
        return odd(n)

def even(n):
    return 1 + hailstone(n // 2)

def odd(n):
    if n == 1:
        return n
    else:
        return 1 + hailstone(3 * n + 1)
