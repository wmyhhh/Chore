def pow(base, exp):
    if exp == 0:
        return 1
    elif exp == 1:
        return base
    elif exp % 2 == 0:
        return pow(base ** 2, exp // 2)
    else:
        return base * pow(base ** 2, exp // 2)
    
def repeat_cube(n, x):
    if n == 0:
        return x
    else:
        x = x ** 3
        n -= 1
    return x