import numpy as np
from arenas.simulator import simulator_with_save
from sklearn.linear_model import LogisticRegression
from agents.MCTS_agent.full_random import FullRandomMCTS
from agents.MCTS_agent.full_random import FullRandomMCTS

# Rules : Heuristics returns the probability of that white wins and must me symetrical 
# Meaning that P(plateau)=1-P(plateau + swap color)
# When P(x)=sigmoid(linear_fct(x)) this mean  linear_fct(x)=-linear_fct(swap x)


def sigmoid(x):
    return 1/(1 + np.exp(-x))

class NaiveEval():

    def __call__(self,board):
        white_score=np.count_nonzero(board.matrix == 1)/np.sum(np.abs(board.matrix))
        if board.current_color=='White':
            return white_score

        else :
            return 1-white_score


class LinearEvaluation():
    def  __init__(self,N=8,save=None):
        self.N=N
        if save!=None:
            # TO DO : load model
            pass
        else:    
            self.model=LogisticRegression(fit_intercept=False,warm_start=True)
            self.model.intercept_= np.zeros((1,))
            self.model.coef_= self.init_coefs()  # type: ignore
            self.model.classes_=np.array([-1,1])

    def __call__(self,board):
        return self.model.predict(self.features(board)).item()  # type: ignore



class Positions(LinearEvaluation):

    def init_coefs(self):                     # For N=8 :     1 2 3 4
                                               #              2 5 6 7
                                               #    	      3 6 8 9
                                               #              4 7 9 10 
        n=self.N//2
        params=np.random.uniform(-1,1,n*(n+1)//2)  # type: ignore
        params[0]=+10
        params[1]=-6
        params[4]=-6
        return params.reshape((1,-1))
    
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
        features=np.array([matrix_sym[i,j] for i in range(n) for j in range(i,n)])
        return features.reshape(1, -1)

   

