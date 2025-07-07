X = [1, 2, 4, 3, 6, 9]
Y = [x for x in X if 60 % x == 0]
print(Y)

def divisor(n):
    return [1] + [x for x in range(2, n + 1) if n % x == 0]

print(divisor(60))