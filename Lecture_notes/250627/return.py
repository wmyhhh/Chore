def end(n,x):
    while n >0 :
        end, n = n % 10, n // 10
        print(end)
        if end == x:
            return None
        
def search(f):
    x = 0
    while not f(x):
        x += 1
    return x
'''
def search(f):
    x = 0
    while True:
        if f(x): # f(x) == True
            return x
        x += 1
'''

def square(x):
    return x*x

def is_three(x):
    return x == 3

def inverse(f):
    return lambda y : search(lambda x: f(x) == y) 
'''
search(lambda)
def lambda(x):
    return f(x) == y
'''


    