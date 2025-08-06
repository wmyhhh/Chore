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


def ordered(s, key = lambda x: x):
    '''
    >>> ordered(Link(1, Link(2, Link(3))))
    True
    >>> ordered(Link(1, Link(2, Link(1))))
    False
    >>> ordered(Link(1, Link(-3, Link(5, Link(-8)))), key = abs)
    True
    '''
    if s is Link.empty or s.rest is Link.empty:
        return True
    elif key(s.first) > key(s.rest.first):
        return False
    else:
        return ordered(s.rest, key)


def merge(s, t):
    '''
    >>> s = Link(1, Link(3))
    >>> t = Link(1, Link(5))
    >>> merge(s, t)
    Link(1,Link(1,Link(3,Link(5))))
    >>> s
    Link(1,Link(3))
    >>> t
    Link(1,Link(5))
    
    '''
    if s is Link.empty:
        return t
    elif t is Link.empty:
        return s
    elif s.first <= t.first:
        return Link(s.first, merge(s.rest, t))
    else:
        return Link(t.first, merge(s, t.rest))

def merge_in_place(s, t):
    '''
    >>> s = Link(1, Link(6))
    >>> t = Link(1, Link(5))
    >>> merge_in_place(s, t)
    Link(1,Link(1,Link(5,Link(6))))
    >>> s
    Link(1,Link(1,Link(5,Link(6))))
    >>> t
    Link(1,Link(5,Link(6)))
    
    '''
    if s is Link.empty:
        return t
    elif t is Link.empty:
        return s
    elif s.first <= t.first:
        #return Link(s.first, merge(s.rest, t))
        s.rest = merge_in_place(s.rest, t)
        return s
    else:
        #return Link(t.first, merge(s, t.rest))
        t.rest = merge_in_place(s, t.rest)
        return t
