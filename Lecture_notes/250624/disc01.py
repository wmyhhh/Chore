# is prime?
def is_prime(n):
    """
    >>> is_prime(10)
    False
    >>> is_prime(7)
    True
    >>> is_prime(1) # one is not a prime number!!
    False
    """
    "*** YOUR CODE HERE ***"
    i = 1
    j = True
    if n == 1:
        j = False
    while i < n//2:
        i+=1
        if n%i == 0:
           j = False
    return j

'''
solution
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True
'''

# unique digits
def unique_digits(n):
    """Return the number of unique digits in positive integer n.

    >>> unique_digits(8675309) # All are unique
    7
    >>> unique_digits(13173131) # 1, 3, and 7
    3
    >>> unique_digits(101) # 0 and 1
    2
    """
    "*** YOUR CODE HERE ***"
    cnt = 0
    while n>0:
        d = n%10
        n = n//10
        if has_digit(n,d) != True:
            cnt += 1
    return cnt

def has_digit(n, k):
    """Returns whether k is a digit in n.

    >>> has_digit(10, 1)
    True
    >>> has_digit(12, 7)
    False
    """
    assert k >= 0 and k < 10
    "*** YOUR CODE HERE ***"
    while n>0:
        if n%10 == k:
            return True
        else:
            n = n//10
    return False