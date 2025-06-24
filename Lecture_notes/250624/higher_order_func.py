from math import pi, sqrt

def area(r,cstn):
    return (r**2)*cstn

def square(r):
    return area(r,1)

def circle(r):
    return area(r,pi)

def identity(n):
    return n

def cube(n):
    return n**3

def appro_pi(n):
    return 8/((4*n-3)*(4*n-1))

def inv_sqrt(n):
    return 1/(n**2)

def summation(n,term):
    total,k = 0,1
    while k <= n:
        total, k = total + term(k), k+1
    return total