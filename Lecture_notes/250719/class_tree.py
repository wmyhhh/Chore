class Tree:
    def __init__(self, label, branches = []):
        self.label = label
        for b in branches:
            assert isinstance(b, Tree)
        self.branches = list(branches)

    def is_leaf(self):
        not self.branches

def fib_tree(n):
    if n == 0 or n == 1:
        return Tree(n)
    else:
        left = fib_tree(n - 1)
        right = fib_tree(n - 2)
        fib_n = left.label + right.label
        return Tree(fib_n, [left, right])
    
def leaves(t):
    if t.is_leaf():
        return [t.label]
    else:
        l = []
        for b in t.branches:
            l.extend(leaves(b))
        return l
    
def height(t):
    if t.is_leaf():
        return 0
    else:
        return 1 + max([height(b) for b in t.branches])
    
def prune_tree(t, n):
    t.branches = [b for b in t.branches if t.label != n]
    for b in t.branches:
        prune_tree(b, n)