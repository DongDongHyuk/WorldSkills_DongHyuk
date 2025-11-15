from collections import deque
import random

class Graph:
    def __init__(self,edges):
        self.edges = edges
        self.graph = {}
        for start,end in self.edges:
            end = list(map(int,end.split(',')))
            self.graph[start] = end
            
edge1 = [(0,'1,5,6'),(1,'0,2,7'),(2,'1,3,7'),(3,'2,4'),(4,'3,8,9'),(5,'0,6,10'),(6,'0,5,7,10,12'),
         (7,'1,2,6,8'),(8,'4,7,12,13'),(9,'4,13,14'),(10,'5,6,11,15'),(11,'10,12,15,16'),
         (12,'6,8,11,13,16,18'),(13,'8,9,12,14'),(14,'9,13,18,19'),(15,'10,11,20'),(16,'11,12,17,20'),
         (17,'16,18,22,23'),(18,'12,14,17,19,24'),(19,'14,18,24'),(20,'15,16,21'),(21,'20,22'),
         (22,'17,21,23'),(23,'17,22,24'),(24,'18,19,23')]

Pal = Graph(edge1)

class findPath:
    def __init__(self,start,end,ObstaclePos):
        self.start = start
        self.end = end
        self.ObstaclePos = list(map(int,ObstaclePos.split(',')))

    def bfs(self):
        que = deque([self.start])
        marked = {self.start:'start'}
        rule = lambda n: n not in self.ObstaclePos
        node = None
        while que and node != self.end:
            node = que.popleft()
            for next_node in Pal.graph[node]:
                if next_node not in marked and rule(next_node):
                    marked[next_node] = node
                    que.append(next_node)
        return marked

    def recoding(self,marked):
        node = self.end
        recode = [node]
        while marked[node] != 'start':
            node = marked[node]
            recode.append(node)
        return recode[::-1]
    Path = lambda self: self.recoding(self.bfs())


def random_case():
    marked = []
    result = []
    def Heat(n):
        while n > 4: n -= 5
        return n
    for Row in range(0,11,5):
        while 1:
            pos = random.randrange(Row,Row+5)
            if Heat(pos) not in marked: break
        marked.append(Heat(pos))
        result.append(pos)
    for i in result[0:2]: result.append(i+15)
    while 1:
        st= random.randrange(0,16)
        if Heat(st) not in marked: break
    li = result[:]+[st]
    end = [i for i in range(15,25) if i not in li]
    end = random.choice(end)
    print(st,end,','.join(map(str,result)))
    return st,end,','.join(map(str,result))

keep_len = []
n = int(input('Number of Tests: '))
for ct in range(n):           
    a,b,c = random_case()
    case1 = findPath(a,b,c)
    result = case1.Path()
    keep_len.append(len(result))
    print(result)
    print('----> [{}]'.format(ct+1))
    print('')
print('average of length: {}'.format(sum(keep_len) / n))
