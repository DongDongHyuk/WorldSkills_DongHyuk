printl = lambda li: list(map(lambda a: print(a),li))
IT = [1,2,1,0,0,0,0,2] # 1: 사각 2: 원형
br = [[9,9,9,9,9,9],
       [9,1,1,2,2,9],
       [9,0,0,3,0,9],
       [9,0,3,0,0,9],
       [9,3,0,0,0,9],
       [9,0,0,3,0,9],
       [9,1,2,2,1,9],
       [9,9,9,9,9,9]]

def true_dire(n,dire = []):
    global br
    y = [-1,-1,0,1,1,1,0,-1]
    x = [0,1,1,1,0,-1,-1,-1]
    for i in range(8):
        if IT[i] == n:
            dire.append([y[i],x[i]])
    print("사각" if n == 1 else "원형",dire)
    for y in range(1,7):
        for x in range(1,5):            
            if br[y][x] == n:
                for dr in dire:
                    if br[y+dr[0]][x+dr[1]] == 0:
                        br[y+dr[0]][x+dr[1]] = 7
            

def main():
    true_dire(2)
    printl(br)
    

main()
