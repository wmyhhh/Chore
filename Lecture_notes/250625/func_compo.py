def compo(f,g):
    def h(x):
        return f(g(x))
    return h

def triple(x):
    return 3*x

def square(x):
    return x*x

def make_adder(x):
    def add(k):
        return k+x
    return add