def even(s):
    if len(s) == 0:
        return [[]]
    elif s[0] % 2 == 0:
        return [s[0]] + even(s[1:]) + [[s[0]].extend(even(s[1:]))]
    else:
        return even(s[1:]) + [[s[0]].extend(odd(s[1:]))]
    
def odd(s):
    if len(s) == 0:
        return [[]]
    elif s[0] % 2 == 1:
        return [s[0]] + odd(s[1:]) + [[s[0]].extend(even(s[1:]))]
    else:
        return odd(s[1:]) + [[s[0]].extend(odd(s[1:]))]
    
def subsets(s):
    """Return all subsets of list s."""
    if not s:
        return [[]]
    rest = subsets(s[1:])
    return rest + [[s[0]] + r for r in rest]

def even_sum_subsets(s):
    """Return all subsets of s whose sum is even."""
    all_subs = subsets(s)
    return [sub for sub in all_subs if sum(sub) % 2 == 0]
