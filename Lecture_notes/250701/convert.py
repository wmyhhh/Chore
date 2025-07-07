def split(n):
    return n //10, n % 10

def sum_rec(n):
    if n < 10:
        return n
    else:
        all_but_last, last = split(n)
        return sum_rec(all_but_last) + last

def sum_iter(n):
    sum = 0
    while n > 0:
        n, last = split(n)
        sum += last
    return sum

def sum_iter_rec(n, sum_digit):
    if n == 0:
        return sum_digit
    else:
        n, last = split(n)
        return sum_iter_rec(n, sum_digit + last)

