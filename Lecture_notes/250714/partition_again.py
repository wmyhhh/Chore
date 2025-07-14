def partition1(m, n):
    if m < 0 or n == 0:
        return 0
    elif m == 0:
        return 1
    else:
        return partition1(m - n, n) + partition1(m, n -1)
    
def partition2(m, n):
    if m < 0 or n == 0:
        return []
    else:
        exact_match = []
        if m == n:
            exact_match = [[n]]
        with_n = [p + [n] for p in partition2(m - n, n)] 
        without_n = partition2(m, n - 1)
        return exact_match + with_n + without_n
    
def partition(m,n):
    if n > 0 and m > 0:
        if n == m:
            yield str(n)
        for p in partition(m - n, n):
            yield p + '+' + str(n)
        yield from partition(m, n - 1)