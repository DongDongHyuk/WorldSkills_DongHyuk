def printl(a,string = "none",count = 1):
    for i in range(24):
        print(a[i], " ") if count % 4 == 0 else print(a[i], end = ' ')
        count += 1
        
def Index(li,n,n1,return_num = False):
    if not -1 < n + n1 < 24 or li[n+n1] == 99: return "IndexError"
    if li[n+n1] != 0: return n + n1 if return_num == True else "Not_zero"
    if n1 == -1 and n in [4,8,12,16,20] or n1 == 1 and n in [3,7,11,15,19,23]:
        return "IndexError"
    return n + n1
    
y_x = lambda y,x: ((y-1)*4+x)-1 # convert 

def find_road(li,start = [],arrival = []):
    B = li[:] # 리스트 저장
    A = [99 if i == 9 else 0 for i in li] # 리스트 변환
    count = 1
    A[y_x(start[0],start[1])] = count # 출발 지점
    while A[y_x(arrival[0],arrival[1])] != count:
        for i in range(len(A)):
            if A[i] == count:
                for l in [-4,4,-1,1]:
                    if Index(A,i,l) not in ["IndexError","Not_zero"]:
                        A[Index(A,i,l)] = count + 1
        count += 1
    next_index = y_x(arrival[0],arrival[1])
    for i in list(range(count-1,0,-1)):
        A[next_index] = 1 # 도착 지점
        for l in [-4,4,-1,1]:
            result = Index(A,next_index,l,True)
            if result != "IndexError":
                if A[result] == i and B[result] == 0:
                    a = result; break
                if A[result] == i: a = result
        next_index = a
    return [1 if i == 1 else 9 if i == 99 else 0 for i in A]

ex_list = [2,2,1,1]+[9,0,0,0]+[0,9,0,0]+[0,0,0,9]+[0,0,9,0]+[1,2,2,1] #파레트
printl(find_road(ex_list,[1,1],[6,1]))
