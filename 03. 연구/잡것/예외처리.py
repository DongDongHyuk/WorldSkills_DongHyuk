num = 4
while num != 8:
    try:
        print('\nnum : {}'.format(num))
        for i in range(8):
            print(i)
            if i == num:
                raise Exception('!')
    except:
        num += 1
