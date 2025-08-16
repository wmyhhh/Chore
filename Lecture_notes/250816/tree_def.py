def tree(label, branches = []):
    for b in branches:
        assert is_tree(b),'...'
    return [label] + list(branches)

def is_tree(t):
    if type(t) != list or len(t) < 1:
        return False
    for b in branches(t):
        if not is_tree(b):
            return False
    return True

def is_leaf(t):
    return not branches(t)

def label(t):
    return t[0]

def branches(t):
    return t[1:]


        

