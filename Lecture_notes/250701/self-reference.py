def print_all(x):
    print(x)
    return print_all

def print_sum(x):
    print(x)
    def next_sum(y):
        return print_sum(x+y)
    return next_sum

a = print_sum(2)(4)(6)
print(a)