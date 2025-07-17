def partition1(m, n):
    if m < 0 or n == 0:
        return 0
    elif m == 0:
        return 1
    else:
        return partition1(m - n, n) + partition1(m, n -1)
'''
partition1(5, 3)
├── partition1(2, 3)
│   ├── partition1(-1, 3) → 0
│   └── partition1(2, 2)
│       ├── partition1(0, 2) → 1
│       └── partition1(2, 1)
│           ├── partition1(1, 1)
│           │   ├── partition1(0, 1) → 1
│           │   └── partition1(1, 0) → 0
│           └── partition1(2, 0) → 0
├── partition1(5, 2)
│   ├── partition1(3, 2)
│   │   ├── partition1(1, 2)
│   │   │   ├── partition1(-1, 2) → 0
│   │   │   └── partition1(1, 1)
│   │   │       ├── partition1(0, 1) → 1
│   │   │       └── partition1(1, 0) → 0
│   │   └── partition1(3, 1)
│   │       ├── partition1(2, 1)
│   │       │   ├── partition1(1, 1)
│   │       │   ├── ...
│   │       └── ...
│   └── partition1(5, 1)
│       ├── ...

'''
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