def printf(br,height,width):
    if len(br) != (height * width): raise SizeError
    br = ' '.join(['X' if i == 'x' else ' ' if i == '0' else str(i) for i in br])
    for i in range(height):
        print('',br[width*(i*2):width*((i+1)*2)])
    print('','-'*((width*2)-1))

