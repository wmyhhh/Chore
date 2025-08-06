class Link:
    empty = ()
    def __init__(self, first, rest = empty):
        assert rest == Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest:
            repr_rest = ',' + repr(self.rest)
        else:
            repr_rest = ''
        return 'Link(' + repr(self.first) + repr_rest + ')'
    
    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

def strange_loop():
    """Return a Link s for which s.rest.first.rest is s.

    >>> s = strange_loop()
    >>> s.rest.first.rest is s
    True
    """
    "*** YOUR CODE HERE ***"
    s = Link(1, Link(3))
    s.rest.first = Link(s.rest.first, s)
    return s

def sum_rec(s, k):
    """Return the sum of the first k elements in s.

    >>> a = Link(1, Link(6, Link(8)))
    >>> sum_rec(a, 2)
    7
    >>> sum_rec(a, 5)
    15
    >>> sum_rec(Link.empty, 1)
    0
    """
    # Use a recursive call to sum_rec; don't call sum_iter
    "*** YOUR CODE HERE ***"
    if s is Link.empty:
        return 0
    elif k == 0:
        return 0
    else:
        return s.first + sum_rec(s.rest, k - 1)

def sum_iter(s, k):
    """Return the sum of the first k elements in s.

    >>> a = Link(1, Link(6, Link(8)))
    >>> sum_iter(a, 2)
    7
    >>> sum_iter(a, 5)
    15
    >>> sum_iter(Link.empty, 1)
    0
    """

    # Don't call sum_rec or sum_iter
    "*** YOUR CODE HERE ***"
    cnt = 0
    while k > 0 and s is not Link.empty:
        cnt, s, k = cnt + s.first, s.rest, k - 1
    return cnt
    
def overlap(s, t):
    """For increasing s and t, count the numbers that appear in both.

    >>> a = Link(3, Link(4, Link(6, Link(7, Link(9, Link(10))))))
    >>> b = Link(1, Link(3, Link(5, Link(7, Link(8)))))
    >>> overlap(a, b)  # 3 and 7
    2
    >>> overlap(a.rest, b)  # just 7
    1
    >>> overlap(Link(0, a), Link(0, b))
    3
    """
    "*** YOUR CODE HERE ***"
    ''' 
    if s is Link.empty or t is Link.empty:
        return 0
    elif s.first == t.first:
        return 1 + overlap(s.rest, t.rest)
    elif s.first <= t.first:
        return overlap(s.rest, t)
    else:
        return overlap(s, t.rest)'''
    cnt = 0
    while not (s is Link.empty or t is Link.empty):
        if s.first == t.first:
            cnt += 1
            s, t = s.rest, t.rest
        elif s.first <= t.first:
            s, t = s.rest, t
        else:
            s, t = s, t.rest
    return cnt

def display(s, k=10):
    """Print the first k digits of infinite linked list s as a decimal.

    >>> s = Link(0, Link(8, Link(3)))
    >>> s.rest.rest.rest = s.rest.rest
    >>> display(s)
    0.8333333333...
    """
    assert s.first == 0, f'{s.first} is not 0'
    digits = f'{s.first}.'
    s = s.rest
    for _ in range(k):
        assert s.first >= 0 and s.first < 10, f'{s.first} is not a digit'
        digits += str(s.first)
        s = s.rest
    print(digits + '...')

def divide(n, d):
    """Return a linked list with a cycle containing the digits of n/d.

    >>> display(divide(5, 6))
    0.8333333333...
    >>> display(divide(2, 7))
    0.2857142857...
    >>> display(divide(1, 2500))
    0.0004000000...
    >>> display(divide(3, 11))
    0.2727272727...
    >>> display(divide(3, 99))
    0.0303030303...
    >>> display(divide(2, 31), 50)
    0.06451612903225806451612903225806451612903225806451...
    """
    assert n > 0 and n < d
    result = Link(0)  # The zero before the decimal point
    "*** YOUR CODE HERE ***"
    seen = {}  # maps remainder -> node
    p = result
    remainder = n
    while remainder != 0:
        if remainder in seen:
            # 余数重复，说明开始循环了
            p.rest = seen[remainder]
            break
        seen[remainder] = p.rest  # 注意是将下一位节点的位置记录下来（即即将创建的位置）
        remainder *= 10
        digit = remainder // d
        remainder = remainder % d
        p.rest = Link(digit)
        p = p.rest

    return result

def divide_(n, d):
    """Return a linked list with a cycle containing the digits of n/d."""
    assert n > 0 and n < d
    result = Link(0)  # The zero before the decimal point
    p = result
    seen = {}  # key: remainder, value: Link node

    remainder = n
    while remainder != 0:
        if remainder in seen:
            # Create cycle by pointing to the earlier node
            p.rest = seen[remainder]
            break
        seen[remainder] = p  # Save current node for this remainder

        remainder *= 10
        digit = remainder // d
        remainder %= d

        p.rest = Link(digit)
        p = p.rest

    return result
