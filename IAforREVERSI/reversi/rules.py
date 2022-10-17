import numpy as np
#from .board import Board
from board import Board

class Rules():

    def __init__(self,N=8):
        assert N%2==0
        self.N=N
        
    def init_board(self):
        matrix=np.zeros((self.N,self.N))
        center=self.N//2

        kernel=np.zeros((2,2))
        kernel[0,0]=-1
        kernel[1,1]=-1
        kernel[1,0]=+1
        kernel[0,1]=+1

        matrix[center-1:center+1,center-1:center+1]=kernel

        return Board(matrix,'white')

    def list_valid_moves(self,board):
        return None
    
    def check_valid(self,board,move):
        return None

    def apply_move(self,board,move):
        board.matrix=None
        board.current_color=None
    


std_rules=Rules(N=8)
start_board=std_rules.init_board()
print(start_board.matrix)
