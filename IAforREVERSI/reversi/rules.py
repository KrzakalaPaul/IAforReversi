import numpy as np
#from sklearn import neighbors
#from scipy import ndimage
from .board import Board
from time import time

class Rules():

    def __init__(self,N=8):
        assert N%2==0
        self.N=N
        #self.neighbors_kernel=np.zeros((3,3),dtype='i')+1
        #self.neighbors_kernel[1,1]=0
        
    def init_board(self):
        dtype='i'
        matrix=np.zeros((self.N,self.N),dtype=dtype)
        center=self.N//2

        kernel=np.zeros((2,2),dtype=dtype)
        kernel[0,0]=+1
        kernel[1,1]=+1
        kernel[1,0]=-1
        kernel[0,1]=-1

        matrix[center-1:center+1,center-1:center+1]=kernel

        return Board(matrix,'Black')
    
    # Version "Optimisé"
    """
    def list_valid_moves(self,board):
        if board.current_color=='White':
            occupied=np.where(board.matrix==-1,1,0)
        else:
            occupied=np.where(board.matrix==1,1,0)
        potential_move=ndimage.convolve(occupied, self.neighbors_kernel, mode='constant', cval=0)
        potential_move=np.where(potential_move>0)  # type: ignore
        List=[]
        for a,b in zip(potential_move[0],potential_move[1]):
            if self.check_valid(board,(a,b)):
                List.append((a,b))
        return List
    """
    def list_valid_moves(self,board):
        List=[]
        for a in range(self.N):
            for b in range(self.N):
                if self.check_valid(board,(a,b)):
                    List.append((a,b))
        return List
    
    def check_valid(self,board,move):
        
        matrix=board.matrix
        if matrix[move]!=0:
            return False

        if board.current_color=='White':
            ally,ennemy=1,-1
        else:
            ally,ennemy=-1,1
        
        
        a,b=move

        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i,j)!=(0,0):
                    """
                    #This piece of code is x2 longer that the next one !
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

                    """
                    posx=a+i
                    posy=b+j

                    ennemy_captured=False

                    while 0<=posx<self.N and 0<=posy<self.N :
                        value=matrix[posx,posy]
                        if value==ennemy:
                            ennemy_captured=True
                        else:
                            if value==ally and ennemy_captured==True:
                                return True 
                            break
                        posx+=i
                        posy+=j
                    
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
                    
                    '''
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
                    '''

                    posx=a+i
                    posy=b+j

                    ennemy_seen=False
                    ennemy_captured=False

                    while 0<=posx<self.N and 0<=posy<self.N :
                        value=board.matrix[posx,posy]
                        if value==ennemy:
                            ennemy_seen=True
                        else:
                            if value==ally and ennemy_seen==True:
                                ennemy_captured=True 
                            break
                        posx+=i
                        posy+=j

                    if ennemy_captured==True:
                        
                        posx=a+i
                        posy=b+j

                        while True :
                            
                            board.matrix[posx,posy]=ally
                            posx+=i
                            posy+=j

                            value=board.matrix[posx,posy]
                            
                            if value==ally:
                                break
                        

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

        

    def white_win(self,board):
        assert board.current_color==None
        white_avantage=np.sum(board.matrix)
        if white_avantage>=0:
            return 1
        else :
            return 0
        

