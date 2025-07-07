def sum_list(s):
    if len(s) == 0:
        return 0
    else:
        return s[0] + sum_list(s[1:])
    
def large_sum(s, n):
    if len(s) == 0:
        return []
    elif s[0] > n:
        return large_sum(s[1:], n)
    else:
        s0 = s[0]
        with_s0 = [s0] + large_sum(s[1:], n-s0)
        without_s0 = large_sum(s[1:], n)
        if sum_list(with_s0) > sum_list(without_s0):
            return with_s0
        else:
            return without_s0