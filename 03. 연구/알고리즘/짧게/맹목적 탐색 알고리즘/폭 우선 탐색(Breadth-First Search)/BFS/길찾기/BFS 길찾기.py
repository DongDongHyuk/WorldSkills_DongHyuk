from collections import deque

case1 = [0,9,0,9,9,9,0,9,0,9,
         0,0,0,9,0,9,0,9,0,0,
         0,9,0,0,0,0,0,9,9,0,
         0,9,0,9,0,0,0,0,0,0,
         0,0,0,0,9,9,9,0,9,0,
         0,9,9,0,9,0,9,0,9,0,
         0,0,9,0,0,0,9,0,0,0,
         0,0,9,0,9,0,9,0,9,0,
         0,0,0,0,9,0,9,0,9,0,
         0,9,0,9,9,0,9,0,9,0]

def downlevel(pos: str): # 11 -> 0
    y,x = map(int,pos.split())
    return ((y-1)*10+x)-1

def uplevel(pos: int): # 0 -> 11
    y = 1 + pos // 10; x = 1 + pos % 10
    return ''.join([str(y),str(x)])

def TrueDirections(li: list,pos: int):
    result = []
    rule = lambda n: bool(li[n] == 0)
    if pos not in list(range(10)) and rule(pos - 10): result.append(pos - 10) # up
    if pos not in list(range(90,100)) and rule(pos + 10): result.append(pos + 10)  # down
    if pos not in list(range(0,91,10)) and rule(pos - 1): result.append(pos - 1)  # left
    if pos not in list(range(9,100,10)) and rule(pos + 1): result.append(pos + 1) # right
    return result    

def BFS(li: list,s: str,y: str):
    start = downlevel(s)
    arrival = downlevel(y)
    marked = {start: "start"}
    que = deque()
    que.append(start)
    while que and arrival not in marked:
        node = que.popleft()
        for True_nodes in (TrueDirections(li,node)):
            if True_nodes not in marked:
                marked[True_nodes] = node
                que.append(True_nodes)
    return marked

def recoding(marked: dict,s: str,y: str):
    start = downlevel(s)
    arrival = downlevel(y)
    recode = []
    node = arrival
    while node != start:
        recode.append(node)
        node = marked[node]
    recode.append(start)
    return recode[::-1]

def print_recode(li:list, recode: list):
    for i in recode: li[i] = '>'
    convert = lambda n: ' ' if (not n) else '0' if n == 9 else n
    li = list(map(convert,li))
    count = 0
    for i in li:
        count += 1
        if not count % 10: print(i)
        else: print(i, end = ' ')

def main(case: list,start,arrival):    
    marked = BFS(case,start,arrival)
    recode = recoding(marked,start,arrival)
    print_recode(case,recode)

main(case1,'1 1','10 6')
