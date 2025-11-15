for i in li0:
    curli = [m[i] for i in li0 if m[i] != '0']
    leafli = [leaf[i] for i in li0 if leaf[i] in curli]  
    pack = m[i]
    if pack != '0':
        n = leafli.index(pack)+1
        fpack = leafli[n % len(curli)]
        n = curli.index(pack)+1
        if curli[n % len(curli)] == fpack:
            continue

        print('pack ->',pack)
        print('front pack ->',fpack)
        print('curli ->',curli)
        print('leafli ->',leafli)

        m = sort(m,leaf,pos1,pack,0)
        m,step = exc(m,pos0,pos1)
        res.append(step)

        n = li0.index(pos1)+1
        m = sort(m,leaf,li0[n % 8],fpack,0)
        m = bfs(1,m,leaf,pos1,'0')
        m,step = exc(m,pos1,pos0)
        res.append(step)

        printf(m,4,4)
        printf(leaf,4,4)
        
# --> 순서를 교체하는 과정에서 이전에 맞춘 순서가 바뀜

##            # 순서 맞춘 뒤 정렬 파트
##            if pos0 in hold:
##                fix.remove(hold[pos0])
##                del hold[pos0]
##            m = bfs(3,m,leaf,li0,li1,pos0)
##            fix.append(pos0)
##            for i in li0:
##                if i not in hold and leaf[i] != '0':
##                    m = bfs(3,m,leaf,li0,li1,i)
##                    fix.append(i)
##            for i in hold:
##                fix.remove(hold[i])
##            if m[pos0] == '0':
##                fix.remove(pos0)
##            m = bfs(1,m,leaf,-1,-1)
