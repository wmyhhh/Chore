a = 1
def f(g):
    a = 2
    return lambda y : a * g(y)

k = f(lambda y : a + y)