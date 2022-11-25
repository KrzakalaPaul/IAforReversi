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

        board=Board(matrix,'Black')
        board.frontier=set()  # type: ignore
        for i in [-1,0,1,2]:
            for j in [-1,0,1,2]:
                board.frontier.add((center-1+i,center-1+j))
        for i in [0,1]:
            for j in [0,1]:
                board.frontier.remove((center-1+i,center-1+j))

        board.valid_moves=self.list_valid_moves(board)

        return board
    
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
        for move in board.frontier:
            if self.check_valid_from_empty(board,move):
                List.append(move)
        return List
    
    def check_valid_from_empty(self,board,move):
        
        matrix=board.matrix

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

    def check_valid(self,board,move):
        
        if board.matrix[move]==0:
            return self.check_valid_from_empty(board,move)
        else:
            return False
        
      

    # TO DO :
    def apply_move(self,board,move):

        if board.current_color=='White':
            ally,ennemy=1,-1
        else:
            ally,ennemy=-1,1

        board.matrix[move]=ally
        
        a,b=move
        dist_x_plus=self.N-a-1
        dist_x_minus=a
        dist_y_plus=self.N-b-1
        dist_y_minus=b

        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i,j)!=(0,0):

                    if j==1:
                        dist_y=dist_y_plus
                    elif j==-1:
                        dist_y=dist_y_minus
                    else:
                        dist_y=self.N
                    
                    if i==1:
                        dist_x=dist_x_plus
                    elif i==-1:
                        dist_x=dist_x_minus
                    else:
                        dist_x=self.N

                    dist=min(dist_x,dist_y)

                    posx=a+i
                    posy=b+j

                    ennemy_seen=False
                    ennemy_captured=False

                    dist_ally=0

                    for _ in range(dist):
                        value=board.matrix[posx,posy]
                        if value==ennemy:
                            ennemy_seen=True
                        else:
                            if value==ally and ennemy_seen:
                                ennemy_captured=True 
                            break
                        posx+=i
                        posy+=j
                        dist_ally+=1

                    if ennemy_captured==True:
                        
                        posx=a+i
                        posy=b+j

                        for _ in range(dist_ally):
                            board.matrix[posx,posy]=ally
                            posx+=i
                            posy+=j
  

        # Update Player
        if board.current_color=='White':
            board.current_color='Black'
        else:
            board.current_color='White'

        # Update Frontier
        board.frontier.remove(move)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (i,j)!=(0,0):
                    x=a+i
                    y=b+j
                    if (0<=x<self.N) and (0<=y<self.N):
                        if board.matrix[x,y]==0: 
                            board.frontier.add((a+i,b+j))

        # Can the opponent move ?
        new_moves=self.list_valid_moves(board)
        board.valid_moves=new_moves

        if len(new_moves)==0:

            if board.current_color=='White':
                board.current_color='Black'
            else:
                board.current_color='White'

            new_moves=self.list_valid_moves(board)
            board.valid_moves=new_moves

            if len(new_moves)==0:
                board.current_color=None

        

    def white_win(self,board):
        assert board.current_color==None
        white_avantage=np.sum(board.matrix)
        if white_avantage==0:
            return 0.5
        elif white_avantage>0:
            return 1
        else :
            return 0
        

