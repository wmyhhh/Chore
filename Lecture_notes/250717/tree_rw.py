def tree(label, branches = []):
    for branch in branches:
        assert is_tree(branch), '...'
    return [label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(t):
    if type(t) != list or len(t) < 1:
        return False
    for b in branches(t):
        if not is_tree(b):
            return False
    return True

def is_leaf(t):
    return not branches(t)

def fib_tree(n):
    if n <= 1:
        return tree(n)
    else:
        left, right = fib_tree(n - 1), fib_tree(n - 2)
        return tree(label(left) + label(right), [left, right])
    
def count_leaves(t):
    if is_leaf(t):
        return 1
    else:
        return sum(count_leaves(b) for b in branches(t))
    
def leaves(t):
    if is_leaf(t):
        return [label(t)] # t?
    else:
        return sum([leaves(b) for b in branches(t)], [])
def wrong_leaves(t):
    if is_leaf(t):
        return t
    else:
        return sum([leaves(b) for b in branches(t)], [])
    
def increment_leaves(t):
    if is_leaf(t):
        return tree(label(t) + 1) # [label(t) + 1]?
    else:
        bs = (increment_leaves(b) for b in branches(t))
        return tree(label(t), bs)
    
def increment(t):
    return tree(label(t) + 1, [increment(b) for b in branches(t)])
    
