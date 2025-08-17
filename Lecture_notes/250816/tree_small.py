from  tree_def_class import *

def smalls(t):
    '''
    'take in a tree and return the subtrees that is not a leaf whose label is smaller than all of its descendents'
    >>> a = Tree(1, [Tree(4, [Tree(4), Tree(5)]), Tree(3, [Tree(0, [Tree(2)])])])
    >>> len(smalls(a))
    1
    >>> b = Tree(2, [Tree(0, [Tree(2, [Tree(4), Tree(1)])]), Tree(1, [Tree(2, [Tree(1), Tree(4)]), Tree(0, [Tree(1)])])])
    >>> len(smalls(b))
    2
    '''
    result = []
    # keep track of the smallest node in its descendent & append sth into result
    def process(t):
        if t.is_leaf():
            return t.label
        else:
            smallest = min([process(b) for b in t.branches])
            if t.label < smallest:
                result.append(t)
            return min(t.label, smallest)
    process(t)
    return result
            



