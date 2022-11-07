import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import pickle

from .rules import Rules
from sklearn import neighbors
from scipy import ndimage

# Rules : Heuristics returns the probability of that white wins and must me symetrical 
# Meaning that P(plateau)=1-P(plateau + swap color)
# When P(x)=sigmoid(linear_fct(x)) this mean  linear_fct(x)=-linear_fct(swap x)

# BASIC CLASS

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
    def  __init__(self,N=8,save=None,scaling=True):

        self.N=N
        lr=LogisticRegression(fit_intercept=False,warm_start=True,max_iter=1000)
        lr.intercept_= np.zeros((1,))
        lr.classes_=np.array([0,1])
        self.lr=lr  
        if scaling:
            self.model= make_pipeline(StandardScaler(),self.lr)
        else:
            self.model=self.lr
        #self.model=LogisticRegression(fit_intercept=False,warm_start=True,max_iter=1000)

        if save!=None:
            self.load(save)
        else:
            self.lr.coef_= self.init_coefs()  # type: ignore
    
    def save(self,path):
        pickle.dump(self.model, open(path, 'wb'))
        #np.save(path,eval_fct.model.coef_)

    def print(self):
        print(self.lr.coef_)

    def load(self,filename):
        self.model=pickle.load(open(filename, 'rb'))

    def __call__(self,board):
        return self.model.predict_proba(self.features(board))[0,1].item()  # type: ignore


class Positions(LinearEvaluation):

    def __init__(self,N=8,save=None):
        super().__init__(N=N,save=save)
        n=N//2
        self.dim=n*(n+1)//2

    def init_coefs(self):                     # For N=8 :     1 2 3 4
                                               #              2 5 6 7
                                               #    	      3 6 8 9
                                               #              4 7 9 10 
        n=self.N//2
        params=np.random.uniform(-1,1,n*(n+1)//2)  # type: ignore
        params[0]=+3
        params[1]=-1
        params[4]=-1
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


# BASIC HEURISTICS

#from sklearn import neighbors
#from scipy import ndimage

def mobility(board,rules):

    board_black=board.copy()
    board_black.current_color='Black'
    black_mobility=len(rules.list_valid_moves(board_black))

    board_white=board.copy()
    board_white.current_color='White'
    white_mobility=len(rules.list_valid_moves(board_white))

    return (white_mobility-black_mobility)/(white_mobility+black_mobility+1e-6)

neighbors_kernel=np.zeros((3,3))+1
neighbors_kernel[1,1]=0

def potential_mobility(board):

    matrix=board.matrix
    empty=(matrix==0)

    black_matrix=np.where(matrix==-1,1,0)
    black_adj=ndimage.convolve(black_matrix, neighbors_kernel, mode='constant', cval=0)
    white_potential=(black_adj*empty>0).sum()

    white_matrix=np.where(matrix==1,1,0)
    white_adj=ndimage.convolve(white_matrix, neighbors_kernel, mode='constant', cval=0)
    black_potential=(white_adj*empty>0).sum()

    return (white_potential-black_potential)/(white_potential+black_potential)


def corner_count(board): 
    matrix=board.matrix
    corners=(matrix[0,0]+matrix[-1,0]+matrix[0,-1]+matrix[-1,-1])/4
    return corners


def precorners_count(board):
    matrix=board.matrix
    N=len(matrix)
    precorners=0
    precorners+=(matrix[1,1]+matrix[1,0]+matrix[0,1])*(1-np.abs(matrix[0,0]))
    precorners+=(matrix[-2,-2]+matrix[-1,-2]+matrix[-2,-1])*(1-np.abs(matrix[-1,-1]))
    precorners+=(matrix[0,-2]+matrix[1,-2]+matrix[1,-1])*(1-np.abs(matrix[0,-1]))
    precorners+=(matrix[-2,0]+matrix[-2,1]+matrix[-1,1])*(1-np.abs(matrix[-1,0]))
    return precorners


def corner_stability(board): #Number of Stable Edge 
        matrix=board.matrix
        N=len(matrix)
        corners=(matrix[0,0]+matrix[-1,0]+matrix[0,-1]+matrix[-1,-1])/4

        line_min=0
        full=True
        while full and line_min<N:
            line=matrix[line_min,:]
            zeros=line.size - np.count_nonzero(line)
            if zeros==0:
                line_min+=1
            else:
                full=False

        if line_min==N:
            print('Evaluating A Final Board')

        
        line_max=N
        full=True
        while full:
            line=matrix[line_max-1,:]
            zeros=line.size - np.count_nonzero(line)
            if zeros==0:
                line_max-=1
            else:
                full=False


        col_min=0
        full=True
        while full:
            line=matrix[:,col_min]
            zeros=line.size - np.count_nonzero(line)
            if zeros==0:
                col_min+=1
            else:
                full=False

        col_max=N
        full=True
        while full:
            line=matrix[:,col_max-1]
            zeros=line.size - np.count_nonzero(line)
            if zeros==0:
                col_max-=1
            else:
                full=False

        # For each corner : if it is occupied, check if it induce other stable disc

        mini_matrix=matrix[line_min:line_max,col_min:col_max]
        mini_stable_matrix=np.zeros_like(mini_matrix)
        
        if mini_matrix[0,0]!=0:

            limit=np.inf
            a=0
            b=0
            color=mini_matrix[0,0]

            while limit!=0:
                a=0
                while a<limit and mini_matrix[a,b]==color:
                    mini_stable_matrix[a,b]=1
                    a+=1
                limit=a
                b+=1


        if mini_matrix[-1,0]!=0:

            limit=np.inf
            a=0
            b=0
            color=mini_matrix[-1,0]

            while limit!=0:
                a=0
                while a<limit and mini_matrix[-a-1,b]==color:
                    mini_stable_matrix[-a-1,b]=1
                    a+=1
                limit=a
                b+=1

        if mini_matrix[0,-1]!=0:

            limit=np.inf
            a=0
            b=0
            color=mini_matrix[0,-1]

            while limit!=0:
                a=0
                while a<limit and mini_matrix[a,-b-1]==color:
                    mini_stable_matrix[a,-b-1]=1
                    a+=1
                limit=a
                b+=1

        if mini_matrix[-1,-1]!=0:

            limit=np.inf
            a=0
            b=0
            color=mini_matrix[-1,-1]

            while limit!=0:
                a=0

                while a<limit and mini_matrix[-a-1,-b-1]==color:
                    mini_stable_matrix[-a-1,-b-1]=1
                    a+=1
                
                limit=a
                b+=1


        stable_matrix=np.zeros_like(matrix)+1    # 1 for stable, 0 for instable 
        stable_matrix[line_min:line_max,col_min:col_max]=mini_stable_matrix

        corners=(matrix[0,0]+matrix[-1,0]+matrix[0,-1]+matrix[-1,-1])

        return np.sum(stable_matrix*matrix)-corners


class Three(LinearEvaluation): 

    def __init__(self,game_states=3,N=8,save=None,scaling=True):

        self.time_codes=np.linspace(0,N**2,game_states+1)
        self.game_states=game_states
        self.dim=3*game_states
        self.rules=Rules(N)

        super().__init__(N=N,save=save,scaling=scaling)

    def init_coefs(self):                   
        params=np.array([1,1,1]*self.game_states)
        return params.reshape((1,-1))

    
    def features(self,board):

        n_moves=np.sum(np.abs(board.matrix))
        
        # Looking for time_code : 
        t=0
        while n_moves>self.time_codes[t+1]:
            t+=1

        mob=mobility(board,self.rules)
        stable=corner_stability(board)
        corners=corner_count(board)
        features=np.zeros(self.dim)
        features[3*t:3*t+3]=np.array([mob,corners,stable])

        return features.reshape(1, -1)



class Four(LinearEvaluation): 

    def __init__(self,game_states=3,N=8,save=None,scaling=True):

        self.time_codes=np.linspace(0,N**2,game_states+1)
        self.game_states=game_states
        self.dim=4*game_states
        self.rules=Rules(N)

        super().__init__(N=N,save=save,scaling=scaling)


    def init_coefs(self):                   
        params=np.array([1,1,1,-0.5]*self.game_states)
        return params.reshape((1,-1))

    def features(self,board):
        
        n_moves=np.sum(np.abs(board.matrix))
        
        # Looking for time_code : 
        t=0
        while n_moves>self.time_codes[t+1]:
            t+=1
         
        mob=mobility(board,self.rules)
        n_stable=corner_stability(board)
        n_corners=corner_count(board)
        n_precorners=precorners_count(board)

        features=np.zeros(self.dim)
        features[4*t:4*t+4]=np.array([mob,n_corners,n_precorners,n_stable])
        return features.reshape(1, -1)

    
class Five(LinearEvaluation):

    def __init__(self,game_states=3,N=8,save=None,scaling=True):

        self.time_codes=np.linspace(0,N**2,game_states+1)
        self.game_states=game_states
        self.dim=5*game_states
        self.rules=Rules(N)

        super().__init__(N=N,save=save,scaling=scaling)


    def init_coefs(self):                   
        params=np.array([1,1,1,0.2,-0.2]*self.game_states)
        return params.reshape((1,-1))

    def features(self,board):
        
        n_moves=np.sum(np.abs(board.matrix))
        
        # Looking for time_code : 
        t=0
        while n_moves>self.time_codes[t+1]:
            t+=1
         
        mob=mobility(board,self.rules)
        pot_mob=potential_mobility(board)
        n_stable=corner_stability(board)
        n_corners=corner_count(board)
        n_precorners=precorners_count(board)

        features=np.zeros(self.dim)
        features[5*t:5*t+5]=np.array([mob,pot_mob,n_corners,n_precorners,n_stable])
        return features.reshape(1, -1)