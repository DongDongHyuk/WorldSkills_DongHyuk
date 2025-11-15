def test(m,p=-1):
    pack = m[0] if p is -1 else p
    print(pack is '1')

test('1')
test('1','1')
