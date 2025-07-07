numeral = {'I': 1, 'V': 5, 'X': 10}
x = list(numeral)
y = list(numeral.values())
print(x,y)

dic = {1: [1, 3], 2: 'str'}
a = dic[1]

def index(key, value, match):
    return {k: [i for i in value if match(k,i)] for k in key }

new_dic = index([1, 7, 9], range(30, 50), lambda k, v: v % k == 0)
print(new_dic)

def search(f):
    x = 0
    while not f(x):
        x += 1
    return x

def reverse(f):
    def g(y):
        def equal(x):
            return f(x) == y
        return search(equal)
    return g

def inverse(f):
    return lambda y : search(lambda x: f(x) == y) 

from math import sqrt
square = reverse(sqrt)
print(square(4))