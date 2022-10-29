from .board import Board
import numpy as np
from numpy import sum,abs


# Rules : Heuristics returns the probability of that white wins and must me symetrical 
# Meaning that P(plateau)=1-P(plateau + swap color)
# When P(x)=sigmoid(linear_fct(x)) this mean  linear_fct(x)=-linear_fct(swap x)


def sigmoid(x):
    return 1/(1 + np.exp(-x))

class NaiveEval():

    def __call__(self,board):
        white_score=np.count_nonzero(board.matrix == 1)/sum(abs(board.matrix))
        if board.current_color=='White':
            return white_score

        else :
            return 1-white_score


class LinearEvaluation():
    def  __init__(self,N=8,params=None):
        self.N=N
        if params==None:
            params= self.init_params()  # type: ignore
        self.params=params

    def __call__(self,board):
        return sigmoid(np.inner(self.params,self.features(board))) # type: ignore


    def train(self,H=1,k=1,t=0.1,n_eval=100,n_update=100,resume=False):  
        # H = Rollout horizon
        # k = Number of rollout/eval for evaluation
        # t = time budget for 1 move
        # n_eval = Number of game between update of the parameter
        # n_update = number of parameter update
        # resume = False or directory of training to resume

        if resume:
            # TO DO : load parameter from save
            # Load Pool of opponents
            pass

        else:
            # TO DO : setup save folder, init parameter, save init param in the folder
            # Init Pool of opponents with fullrandom MCTS
            pass


        for update_counter in range(n_update):

            # Setup agent to evaluate

            # Initialize empty dateset board/winner

            for simulation_counter in range(n_eval):

                # Run a game, return list of board 

                # update dataset

            # update param
            # save old params in directory 
            # update pool of opponents

                 pass



class Positions(LinearEvaluation):

    def init_params(self):                     # For N=8 :     1 2 3 4
                                               #               2 5 6 7
                                               #    	       3 6 8 9
                                               #               4 7 9 10 
        n=self.N//2
        params=np.random.uniform(-1,1,n*(n+1)//2)  # type: ignore
        params[0]=+10
        params[1]=-6
        params[4]=-6
        return params
    
    def features(self,board):
        n=self.N//2
        matrix=board.matrix
        #print(matrix[0:n-1,0:n-1])
        #print(np.flip(matrix[n-1:,0:n-1],axis=0))
        #print(np.flip(matrix[0:n-1,n-1:],axis=1))
        #print(np.flip(matrix[n-1:,n-1:],axis=(0,1)))
        matrix_sym=matrix[0:n,0:n]+np.flip(matrix[n:,0:n],axis=0)+np.flip(matrix[0:n,n:],axis=1)+np.flip(matrix[n:,n:],axis=(0,1))
        matrix_sym_copy=matrix_sym.copy()
        np.fill_diagonal(matrix_sym_copy, 0)
        matrix_sym=matrix_sym+matrix_sym_copy.T
        features=[matrix_sym[i,j] for i in range(n) for j in range(i,n)]
        return features

   

