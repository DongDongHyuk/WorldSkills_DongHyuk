import random

def is_solved(board: str):
    if not board:
        return True
    result = 0
    br = list(board)
    for i in range(9):
        count = 0
        pos = br.index(str(i))        
        for j in range(pos,9):
            if int(br[j]) < int(i): count += 1            
        result += count
    return (not result % 2 == 0)

def random_board():
    board = []
    while is_solved(board):
        board = ['0','1','2','3','4','5','6','7','8']
        random.shuffle(board)
    board[board.index('0')] = '_'
    return ''.join(board)

start_state = random_board()
print("start: {}".format(start_state))
