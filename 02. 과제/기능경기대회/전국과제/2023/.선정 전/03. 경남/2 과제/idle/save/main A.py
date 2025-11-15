    if t == 0:
        global ing
        m1 = m[:]
        m2,hli = a
        m1,m2 = map(list,[m1,m2])       # pack exchanging
        for i in range(15):
            if m1[i] in '456':
                j = [j for j in range(15) if m2[j] in '123'][0]
                m1[i],m2[j] = m2[j],m1[i]
                res.append([i,j,m1[i],m2[j]])
        m1,m2 = map(''.join,[m1,m2])
        leaf = []       # making leaf
        for i in range(2):
            m0 = ['0'] * 15
            ct = [-1,0,0,0,0,0,0]
            li = ([j for j in range(15) if leaf[0][j] == '0'] if i else [])+list(range(15)) 
            for j in hli[1-i]+li:
                pack = j // 5 + (3 * i) + 1
                if j not in hli[i] and m0[j] == '0' and ct[pack] < 3:
                    m0[j] = str(pack)
                    ct[pack] += 1
            leaf.append(''.join(m0))
        leaf1,leaf2 = leaf
        for i in range(2):
            ing = i         # now sorting
            m = [m1,m2][i]
            leaf = [leaf1,leaf2][i]            
            for j in [0,1,2,3,4]:
                if j in hli[i] or leaf[j] == '0':
                    m = bfs(1,m,leaf,j,'0')
                    fix.append(j)
                else:
                    m = sort(m,leaf,j)
            m = bfs(1,m,leaf,-1,-1)
            if i:
                m2 = m[:]
            else:
                m1 = m[:]
            fix = []        # fix reset
