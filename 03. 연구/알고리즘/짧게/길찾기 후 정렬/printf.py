def printf(br,height,width):
    if len(br) != height*width:
        return print('lenERROR')
    br = ' '.join([str(i.upper()) for i in br])
    for i in range(height):
        print('',br[width*(i*2):width*((i+1)*2)])
    print('','-'*((width*2)-1))
