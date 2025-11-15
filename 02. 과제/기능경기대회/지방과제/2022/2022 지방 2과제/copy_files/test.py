def solving_puzzle():
    global serch_result,C_1,C_3
    maintain = 0    
    # 거울 배치, C - 3 재배치, C - 1 재배치
    err = [12,0,12] # 오차
    for li in serch_result: # 거울 배치. 재 배치
        for j in range(0,len(li),2):
            s = err[serch_result.index(li)]+li[j] # 옮길 팩 위치 = 오차 + 현재 위치 
            a = err[serch_result.index(li)]+li[j+1]  # 옮길 위치 = 오차 + 다음 위치            

            if maintain == 0: moves(C[s])
            else: maintain = 0
            write(s+1,0)
            movec(trans(C[a],[0,0,1,0,0,0]),C[a])

            if j+2 < len(li) and li[j+1] != li[j+2]: movea(C[a])
            else: maintain = 1
            write(a+1,read(s+1))
            
        if li == serch_result[0]: # 거울 배치 짧게 두번
            buzz(2)
            wait(0.31)
            buzz(2)
            
    for i in [[10,7],[11,8],[22,19],[23,20]]:
        moves(C[i[0]])
        movec(trans(C[i[0]],[0,0,1,0,0,0]),C[i[1]])
        movea(C[i[1]],i[1]+1,3)
    buzz(3) # 완성 부저
