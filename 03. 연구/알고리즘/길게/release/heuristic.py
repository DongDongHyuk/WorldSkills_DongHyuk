"""
    def heu(m):
        ct = 0
        if p != -1:
            s,e = m.index(pk),p
            r1 = src(0,m,s,e)
            ct += len(r1) + (10 * len([i for i in r1 if m[i] not in '0'+pk]))
            r2 = src(-2,m,p,-1)
            isDead = len(r2) > 1
        for i in range(size):
            if m[i] not in '0x':
                y1,x1 = divmod(i,sx)
                y2,x2 = divmod(p if p != -1 else leaf.index(m[i]),sx)
                dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                ct += (10000 * (size - dst) if isDead and i in r2 else -dst) if p != -1 and m[i] != pk else dst
        return ct

    def heu(m):
        ct = 0
        if p != -1:
            s,e = m.index(pk),p
            r1 = src(0,m,s,e)
            rp = len([i for i in r1 if m[i] not in '0'+pk])
            ct += 10000 * rp
            r2 = src(-2,m,p,-1)
            isDead = len(r2) > 1
        for i in range(size):
            if m[i] not in '0x':
                y1,x1 = divmod(i,sx)
                y2,x2 = divmod(p if p != -1 else leaf.index(m[i]),sx)
                dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                ct += (100 * (size - dst) if isDead and i in r2 else -dst) if p != -1 else dst
        if p != -1 and not rp:
            ct = -99999 * (2 if m[p] == pk else 1)
        # if p != -1 and p in src(-1,m,s,-1):
        #     ct = -99999 * (2 if m[p] == pk else 1)
        return ct

    def heu(m):
        ct = 0
        if p != -1:
            s,e = m.index(pk),leaf.index(pk)
            r1 = src(0,m,s,e)
            ct += len(r1)
            ct += 10 * len([i for i in r1 if m[i] not in '0'+pk])
            r2 = src(-2,m,p,-1)
            isDead = len(r2) > 1
        for i in range(size):
            if m[i] not in '0x':
                # 길찾기 ver
                dst = len(src(0,m,i,leaf.index(m[i]) if p == -1 else p))
                # 맨해튼 ver
                # y1,x1 = divmod(i,sx)
                # y2,x2 = divmod(leaf.index(m[i]) if p == -1 else p,sx)
                # dst = (abs(y1 - y2) + abs(x1 - x2)) + 1                
                ct += (dst if p == -1 else (1000 * (size - dst) if isDead and i in r2 else -dst))
        if p != -1 and p in src(-1,m,s,-1):
            ct = -99999 * (2 if m[p] == pk else 1)
        # print('ct ->',ct)
        # print(p,pk)
        # prt(m,6,3)
        # input()
        return ct

    def heu(m):
        ct = 0
        if p != -1:
            e = p
            di = {}
            for i in range(size):
                if m[i] == pk and not fx[i]:
                    di[i] = len([i for i in src(0,m,i,e) if m[i] not in '0'+pk])            
            s = min(di,key=lambda n:di[n])
            rp = di[s]            
            ct += 10000 * rp
            r2 = src(-2,m,p,-1)
            isDead = len(r2) > 1
        for i in range(size):
            if m[i] not in '0x':
                y1,x1 = divmod(i,sx)
                y2,x2 = divmod(p,sx)
                dst = (abs(y1 - y2) + abs(x1 - x2)) + 1
                ct += (100 * (size - dst) if isDead and i in r2 else -dst) if p != -1 else dst
        if p != -1 and not rp:
            ct = -2 ** (30 if m[p] == pk else 20)        
        return ct
"""