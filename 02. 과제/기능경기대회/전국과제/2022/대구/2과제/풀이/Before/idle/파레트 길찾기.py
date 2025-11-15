from collections import deque

class Graph:
    def __init__(self,edges):
        self.edges = edges
        self.graph = {}
        for start,end in self.edges:
            end = list(map(int,end.split(',')))
            self.graph[start] = end
            
edge1 = [(0,'1,5,6'),(1,'0,2'),(2,'1,3,7'),(3,'2,4'),(4,'3,8,9'),(5,'0,10'),(6,'0,7,11'),
        (7,'2,6,8'),(8,'4,7,12,13'),(9,'4,14'),(10,'5,11,15'),(11,'6,10,16'),(12,'6,8,16,18'),
        (13,'8,14,18'),(14,'9,13,19'),(15,'10,20'),(16,'11,17,20'),(17,'16,18,22'),(18,'12,13,17,24'),
        (19,'14,24'),(20,'15,16,21'),(21,'20,22'),(22,'17,21,23'),(23,'22,24'),(24,'18,19,23')]

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

case1 = findPath(0,24,'3,8,12,18,21')
print(case1.Path())

