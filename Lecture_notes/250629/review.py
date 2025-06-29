'''print(print(5))

def delay(arg):
    print('delayed')
    def g():
        return arg
    return g

x = delay(delay)()(6)()
print(x)

print(delay(print)()(4))

from operator import add, mul

def square(x):
    return x * x

def pirate(argg):
    print('gagaga')
    def plunder(argg):
        return argg
    return plunder

x = add(pirate(3)(square)(4),1)
print(x)

pirate(pirate(pirate))(5)(7)'''

def horse(mask):
    horse = mask
    def mask(horse):
        return horse
    return horse(mask)

mask = lambda horse: horse(2)

horse(mask)

def remove(n,digit):
    kept, x = 0, 0
    while n > 0:
        n, end = n // 10, n % 10
        if end != digit:
            kept = kept + end * 10 ** (x)
            x += 1
    return kept
