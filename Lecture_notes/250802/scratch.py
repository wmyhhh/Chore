def perfect(total, n):
    '''
    >>> perfect(9, 1)
    True
    >>> perfect(10, 2)
    True
    >>> perfect(9, 3)
    False
    '''
    def helper(total, n, k):
        if total == 0 and n == 0:
            return True
        if total < k **2:
            return False
        return helper(total, n, k + 1) or helper(total - k ** 2, n - 1, k + 1)

    return helper(total, n, 1)