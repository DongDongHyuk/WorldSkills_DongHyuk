def comparing_li(li,li2,count = 0):
    for i in range(len(li)):
        if li[i] != li2[i]:
            count += 1
    return count

print(comparing_li([1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,3]))
