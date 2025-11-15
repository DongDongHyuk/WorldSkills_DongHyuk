A = [2,1,2,0,1,0,3,1,2]; m_A = [0] * 9
count = 0
for i in [3,2,1,6,5,4,9,8,7]:
    m_A[count] = A[i-1]
    count += 1
print(id(A))
print(id(m_A))

