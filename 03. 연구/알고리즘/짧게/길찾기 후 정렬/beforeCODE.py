from collections import deque

def chn(br, now, new):
      br = list(br)
      if Type == 1:
            if br[new] == 'b':
                  new = new + (new - now)
      br[now],br[new] = br[new],'0'
      return ''.join(br)

def Truedirs(mode=0,br=None,pos=None):
    result = []
    if mode: n_p = [ct for ct,i in enumerate(br) if i == '0' and ct not in fix[1]]
    def rule(br,pos,posN):
        if mode:
            return br[posN] not in fix[0] and posN not in fix[1] #Sorting
        return br[posN] == '0'
    Dir = [-x_size,x_size,-1,1]
    if not mode:
        for i in range(4):
            if pos not in wall[i] and rule(br,None,pos+Dir[i]):
                result.append(pos+Dir[i])
    else:
        for pos in n_p:
            for i in range(4):
                if pos not in wall[i] and rule(br,pos,pos+Dir[i]):
                    result.append(chn(br,pos,pos+Dir[i]))
    return result

def bfs_find_road(br,start,end):
      br = ''.join([i if i == 'x' else '0' for i in br]) # only fixed packs
      que = deque([start])
      marked = {start:'root'}
      pos = None
      while pos != end:
            pos = que.popleft()
            for next_pos in Truedirs(0,br,pos):
                  if next_pos not in marked:
                        marked[next_pos] = pos
                        que.append(next_pos)
      marked['leaf'] = pos
      return marked

def bfs_sort(root,leaf=None,idx=None,pack = None):
      que = deque([root])
      marked = {root:'root'}
      br = root
      def isleaf(br):
            if Type in [0,2]:
                  if idx != None:
                        if pack != None:
                            return br[idx] != pack
                        return br[idx] != leaf[idx]
                  return br != leaf
            else:
                  pack_li = lambda br:[[br[i]for i in range(5)],[br[j]for j in range(10,15)]]
                  a,b = pack_li(br)
                  return not('2' not in a and '1' not in b)
      while isleaf(br):
            br = que.popleft()
            for next_br in Truedirs(1,br): 
                  if next_br not in marked:
                        marked[next_br] = br
                        que.append(next_br)
      marked['leaf'] = br
      if idx != None: fix[1].add(idx)
      return marked

def path(marked):
      br = marked['leaf']
      path = [br]
      while marked[br] != 'root':
            br = marked[br]
            path.append(br)
      return path[::-1]

def converter(result):
      if not len(result): return []
      first,path = result[0],[]
      for second in result[1:]:
            step = [None,None]
            for i in range(len(second)):
                  if first[i] != second[i]:
                        if first[i] =='0': step[1] = i
                        else: step[0] = i
            if None not in step: path.append(step)
            first = second[:]
      return path

def main(root):
      global Type,fix,wall,x_size
      result = [None] * 3

      # A
      Type = 0
      fix = ({'0','x'},set())
      wall = ([0,1,2,3,4,5,6,7,8,9,10,11],[60,61,62,63,64,65,66,67,68,69,70,71],
              [0,12,24,36,48,60],[11,23,35,47,59,71])
      x_size = 12
      br = root[0][0]
      start,end = root[0][1],root[0][2]
      find_road_result = path(bfs_find_road(br,start,end)) # find road result
      sort_result,marked = [],{'leaf':br} # sort result
      for i in find_road_result:
          marked = bfs_sort(marked['leaf'],None,i,'0')
          sort_result += path(marked)
      result[0] = [converter(sort_result),find_road_result]

      # B
      Type = 1
      fix = ({'0','x'},set())
      wall = ([0,1,2,3,4],[10,11,12,13,14],[0,5,10],[4,9,14])
      x_size = 5
      br = root[1]
      sort_result = path(bfs_sort(br))
      result[1] = converter(sort_result)

      # C
      Type = 2
      fix = ({'0','x'},set())
      wall = ([0,1,2],[6,7,8],[0,3,6],[2,5,8])
      x_size = 3
      br = root[2]
      leaf = '123456700'
      sort_result = path(bfs_sort(br,leaf))
      result[2] = converter(sort_result)

      return result

##root = [('09x009990x090009xxx09999999090009x00990999x009x9900x90x999909x909990x909',0,71),
##        '12001xbxxx10202',
##        '642315700']


