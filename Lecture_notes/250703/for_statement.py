liste = [1, 2, 3, 5, 3, 6]
def search(s, value):
    tot = 0
    for i in s:
        if i == value:
            tot += 1
    return tot
print(search(liste, 3))


# sequence unpacking
pairs = [[1, 2], [3, 2], [2, 2], [4, 4]]
tot = 0
for x, y in pairs:
    if x == y:
        tot += 1
print(tot)

a = list(range(4))
print(a)