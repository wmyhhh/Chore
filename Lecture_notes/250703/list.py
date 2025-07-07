from operator import add, mul
list1 = [1, 2, 8]
list2 = [2 // 2, 1 * 2, 2 ** 2]
print(list1, list2)

list3 = list1 + list2 * 2
list4 = add(list1, mul(list2, 2))
print(list3, list4)

list5 = [list1, list3]
print(list5, list5[1], list5[1][2])