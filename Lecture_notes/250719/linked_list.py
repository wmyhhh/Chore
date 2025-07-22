# linked list
# a linked list is either an empty list or a first value and the rest of a linked list
# like a pair
class Link:
    empty = ()
    def __init__(self, first, rest = empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest
# GPT helps:
    def __repr__(self):
        if self.rest is Link.empty:
            return f'Link({self.first})'
        else:
            return f'Link({self.first}, {repr(self.rest)})'
        
    def __str__(self):
        elems = []
        current = self
        while current is not Link.empty:
            elems.append(str(current.first))
            current = current.rest
        return '<' + ' '.join(elems) + '>'
    
'''
>>> s = Link(2, Link(3, Link(4)))
>>> s
Link(2, Link(3, Link(4)))
>>> s.first
2
>>> s.rest.first
3
>>> s.rest.rest.first
4
>>> s.rest.rest.rest
()
>>> s.rest.rest.rest is Link.empty
True
>>> s.rest.rest = Link(7, Link(8, Link(9)))
>>> s
Link(2, Link(3, Link(7, Link(8, Link(9)))))
>>> print(s)
<2 3 7 8 9>
>>> Link(2, s.rest.rest)
Link(2, Link(7, Link(8, Link(9))))'''
