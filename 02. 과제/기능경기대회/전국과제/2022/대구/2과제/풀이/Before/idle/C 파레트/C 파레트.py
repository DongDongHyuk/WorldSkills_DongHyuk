from collections import deque # que

def converting_Bn(n):
    result = []
    while n:
        result.append(n % 2)
        n = n // 2
    result = [2 ** ct for ct,i in enumerate(result) if i]
    return result

def prt(board: str, text = None):
    isSmall = lambda n:"EX" if n == '-1' else ' '+n if (int(n) < 10) else  n
    board = ''.join(map(isSmall,board.split(',')))
    print('',board[:6])
    print('',board[6:12],end = '')
    print(' [{}]'.format(text))
    print('',board[12:18])
    print('','------')

class get_num:
    def __init__(self,board):
        self.board = board

    def 
