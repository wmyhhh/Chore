def tree(lable, branches = []):
    for branch in branches:
        assert is_tree(branch), '。。。'
    return [lable] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    return not branches(tree)

def fib_tree(n):
    if n <= 1:
        return tree(n)
    else:
        left, right = fib_tree(n - 1), fib_tree(n - 2)
        return tree(label(left) + label(right), [left, right])
    
def print_tree(t, indent = 0):
    print(' -- ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

# this works too
def al_print_tree(t, indent = 0):
    print(' ' * indent, label(t))
    for b in branches(t):
        print_tree(b, indent + 1)

def print_tree_pro(t, indent = 0):
    print(' ' * indent + '|')
    print(' ' * (indent + 1) + '----' + str(label(t)))
    for b in branches(t):
        print_tree_pro(b, indent + 1)