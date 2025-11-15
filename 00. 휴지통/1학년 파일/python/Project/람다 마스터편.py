A = [[9 if x == 0 or y == 0 or x == 9 or y == 7 else 0 for x in range(10)]for y in range(8)]
A[3][3] = 5

X = list(map(lambda y: A[y], range(8)))
for i in X:
    print(i)
print('==============================')
X = [[0 if X[y][x] == 5 else X[y][x] for x in range(10)]for y in range(8)]

for i in X:
    print(i)

