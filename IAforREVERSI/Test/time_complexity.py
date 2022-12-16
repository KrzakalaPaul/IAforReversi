### Test time complexity
from reversi.board import Board
from reversi.rules import Rules
from time import time

import numpy as np

def bolean():
    X=np.zeros((8,8), dtype = 'bool')
    X[0,0]=1
    X[0,1]=1   
    t=time()
    for _ in range(10000):
        if X[0,0]==0:
            pass
    print('Bolean Matrix ==')
    print(time()-t)

    t=time()
    for _ in range(10000):
        if not(X[0,0]):
            pass
    print('Full Bolean ==')
    print(time()-t)
    X=np.zeros((8,8), dtype = 'float')
    X[0,0]=1
    X[0,1]=1   
    t=time()
    for _ in range(10000):
        if X[0,0]==0:
            pass
    print('Not Bolean')
    print(time()-t)

    

def moves():
    rules=Rules(N=8)
    board=rules.init_board()

    for _ in range(5):
        move=rules.list_valid_moves(board)[0]
        rules.apply_move(board,move)

    print(board.matrix)
    move=rules.list_valid_moves(board)[0]

    t=time()
    for _ in range(10000):
        rules.apply_move(board.copy(),move)
    print('Apply a valid move')
    print(time()-t)

    t=time()
    for _ in range(10000):
        rules.check_valid(board,move)
    print('Checking a valid move')
    print(time()-t)

    t=time()
    not_valid_move=(4,5)
    assert not(rules.check_valid(board,not_valid_move))
    for _ in range(10000):
        rules.check_valid(board,not_valid_move)
    print('Checking a non valid move')
    print(time()-t)

    list=rules.list_valid_moves(board)
    print(f'number of moves :{len(list)}')


    t=time()
    print(f'frontier lenght: {len(board.frontier)}')
    for _ in range(10000):
        rules.list_valid_moves(board)
    print('List valid moves')
    print(time()-t)



from reversi.heuristics import mobility,potential_mobility,corner_stability,corner_count,precorners_count

def heuristics():

    rules=Rules(N=8)
    board=rules.init_board()

    for _ in range(5):
        move=rules.list_valid_moves(board)[0]
        rules.apply_move(board,move)

    
    t=time()
    eval=mobility(rules)
    for _ in range(10000):
        eval(board)
    print('mob')
    print(time()-t)

    t=time()
    eval=potential_mobility(rules)
    for _ in range(10000):
        eval(board)
    print('pot mob')
    print(time()-t)

    t=time()
    eval=corner_stability(rules)
    for _ in range(10000):
        eval(board)

    print('corner_stability')
    print(time()-t)

    t=time()
    eval=corner_count(rules)
    for _ in range(10000):
        eval(board)
    print('corner_count')
    print(time()-t)
    
    t=time()
    eval=corner_count(rules)
    for _ in range(10000):
        eval(board)
    print('precorners_count')
    print(time()-t)
