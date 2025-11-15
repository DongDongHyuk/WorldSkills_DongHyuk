def printf(br,width,height):        # 파레트 출력
    if len(br) != height*width:
        return print('lenERROR')
    br = ' '.join([str(i.upper()) for i in br])
    for i in range(height):
        print('',br[width*(i*2):width*((i+1)*2)])
    print('','-'*((width*2)-1))

def printS(state,Type):             # 'State' 클래스 출력
    if not Type:
        print('INDEX :')
        print('   ',state.it[0])
        print(' ',state.it[7],' ',state.it[1])
        print(state.it[6],'     ',state.it[2])
        print(' ',state.it[5],' ',state.it[3])
        print('   ',state.it[4])
        print('TURN :',state.turn)
        print('Spin_count :',state.spin_count)
        print('Pack :',','.join(state.pack))
        printf(state.br,4,6)
        print('\n')
    else:
        print('Pack Dire :',state.pack_dire)
        print('move Dire :',state.move_dire)
        printf(state.br[0],3,4)
        printf(state.br[1],4,3)
        print('\n')

