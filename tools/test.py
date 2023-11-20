"""

list1 = [x for x in range(1, 4)]
lsit2 = ["a", "b", "c"]

a = zip(list1, lsit2)

# for i, j in a:
#     print(i, j)

a1 = 13
b = 5
abc = a1 if a1 > b else b
# print(abc)

ad = lambda x, y: x if x > y else y

print(ad(10, 5))
"""
print('abc')

