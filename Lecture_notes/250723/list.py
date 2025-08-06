'''
>>> s = [1, 2]
>>> t = [5, 6]
>>> s.append(t)
>>> s
[1, 2, [5, 6]]
>>> t[1] = 4
>>> t
[5, 4]
>>> s
[1, 2, [5, 4]]
>>> s.extend(t)
>>> s
[1, 2, [5, 4], 5, 4]
>>> t[0] = 3
>>> s
[1, 2, [3, 4], 5, 4]
>>> s = [1, 2]
>>> t = [5, 6]
>>> s.append(t)
>>> s
[1, 2, [5, 6]]
>>> t = [3, 4]
>>> s
[1, 2, [5, 6]]

>>> s = [1, 2]
>>> t = [5, 6]
>>> a = s + [t]
>>> b = a[1:]
>>> a[1] = 9
>>> b[1][1] = 0
>>> s
[1, 2]
>>> t
[5, 0]
>>> a
[1, 9, [5, 0]]
>>> b
[2, [5, 0]]

>>> s = [1, 2]
>>> t =[5, 6]
>>> s = list(t)
>>> t = [3, 4]
>>> s
[5, 6]
>>> s = [1, 2]
>>> t = [5, 6]
>>> s[0:0] = t
>>> s[4:] = t
>>> t[0] = 3
>>> s
[5, 6, 1, 2, 5, 6]
>>> t
[3, 6]

'''

def min_abs(s):
    '''
    >>> min_abs([1, 2, 3])
    [0]
    >>> min_abs([-5, -3, 0, 2, 4, 0])
    [2, 5]
    '''
    return [i for i in range(len(s)) if s[i] == min(map(abs, s))]

def largest_adj(s):
    '''
    >>> largest_adj([-4, -3, -2, 3, 4])
    7
    >>> largest_adj([-3, 2, -2, -1, 3])
    2
    '''
    #return max(s[i] + s[i + 1] for i in range(len(s) - 1))
    return max(a + b for a, b in zip(s[1:], s[:-1]))

def digit_dict(s):
    '''
    >>> digit_dict([3, 4, 21, 56, 76, 999])
    {1: [21], 3: [3], 4: [4], 6: [56, 76], 9: [999]}

    '''
    end = [x % 10 for x in s]
    return {i: [x for x in s if x % 10 == i] for i in range(10) if i in end}

def equal(s):
    '''
    >>> equal([-1, -2, 3, 3, 3, -1, -2])
    True
    >>> equal([-1, -1, 3, 4, 3])
    False
    '''
    #return all(s[y] in s[:y] + s[y + 1:]for y in range(len(s)))
    return min([sum(1 for y in s if x == y) for x in s]) > 1

