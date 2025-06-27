''' Every user-defined func has a parent frame
the parent of a func is the frame in which it was defined
every local frame has a parent frame'''

def make_adder(n):
    def adder(k):
        return k+n
    return adder