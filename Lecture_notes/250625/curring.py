def cur(f):
    def g(x):
        def h(y):
            return f(x,y)
        return h
    return g

def make_adder(x):
    return lambda k: k+x

