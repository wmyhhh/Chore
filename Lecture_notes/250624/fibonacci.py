def fib(n):
    pre,cur = 1,0
    k=0
    while k<n :
        pre,cur = cur,pre+cur
        k += 1
    return cur