def fact_ori(n):
    if n == 1:
        return 1
    else:
        return n * fact_ori(n - 1)
    
def fact_times(n, k):
    '''return k * n * (n - 1) * ... * 1'''
    if n == 0:
        return k
    else:
        return fact_times(n - 1, k * n)
    
def fact(n):
    return fact_times(n, 1)

from tree_rw import *

numbers = tree(1, [tree(3, [tree(4, [tree(5)])])])

haste = tree('h', [tree('a',[tree('t'), tree('s'), tree('p', [tree('p', [tree('y')])])]), tree('e')])

def sum_path(tree, so_far):
    so_far += label(tree)
    if is_leaf(tree):
        print(so_far)
    else:
        for b in branches(tree):
            sum_path(b, so_far)
        