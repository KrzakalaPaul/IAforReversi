import numpy as np
from .board import Board

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

        return Board(matrix,'Black')
    
    # TO DO
    def list_valid_moves(self,board):
        List=[]
        for a in range(self.N):
            for b in range(self.N):
                if self.check_valid(board,(a,b)):
                    List.append((a,b))
        return List
    
    def check_valid(self,board,move):

        if board.current_color=='White':
            ally,ennemy=1,-1
        else:
            ally,ennemy=-1,1
        
        matrix=board.matrix
        if matrix[move]!=0:
            return False
        
        a,b=move

        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i,j)!=(0,0):

                    k=1
                    ally_seen=False
                    ennemy_seen=0
                    bolean_empty=True
                    while 0<=a+k*i<self.N and 0<=b+k*j<self.N and not(ally_seen) and bolean_empty:
                        if matrix[a+k*i,b+k*j]==ally:
                            ally_seen=True
                        elif matrix[a+k*i,b+k*j]==ennemy:
                            ennemy_seen+=1
                        else:
                            bolean_empty=False
                        k+=1

                    if ally_seen==True and ennemy_seen>0:
                        return True
        
        return False

    # TO DO :
    def apply_move(self,board,move):
        if board.current_color=='White':
            ally,ennemy=1,-1
        else:
            ally,ennemy=-1,1

        board.matrix[move]=ally

        a,b=move

        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i,j)!=(0,0):

                    k=1
                    ally_seen=False
                    ennemy_seen=0
                    bolean_empty=True
                    while 0<=a+k*i<self.N and 0<=b+k*j<self.N and not(ally_seen) and bolean_empty:
                        if board.matrix[a+k*i,b+k*j]==ally:
                            ally_seen=True
                        elif board.matrix[a+k*i,b+k*j]==ennemy:
                            ennemy_seen+=1
                        else:
                            bolean_empty=False
                        k+=1

                    
                    if ally_seen==True and ennemy_seen>0:
                        ally_seen=False
                        k=1
                        while ally_seen==False:
                            if board.matrix[a+k*i,b+k*j]==ally:
                                ally_seen=True
                            board.matrix[a+k*i,b+k*j]=ally
                            k+=1

        if board.current_color=='White':
            board.current_color='Black'
        else:
            board.current_color='White'

        # Can the opponent move ?

    
        if self.list_valid_moves(board)==[]:

            if board.current_color=='White':
                board.current_color='Black'
            else:
                board.current_color='White'

            if self.list_valid_moves(board)==[]:
                board.current_color=None

        

    

