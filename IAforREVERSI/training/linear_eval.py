
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import pickle
from reversi.rules import Rules
from sklearn import neighbors
from reversi.heuristics import*

def sigmoid(x):
    return 1/(1 + np.exp(-x))


class LinearEvaluation():
    def  __init__(self,features_list):

        self.N=N
        lr=LogisticRegression(fit_intercept=False,warm_start=True,max_iter=1000)
        lr.intercept_= np.zeros((1,))
        lr.classes_=np.array([0,1])
        self.lr=lr  
        if scaling:
            self.model= make_pipeline(StandardScaler(),self.lr)
        else:
            self.model=self.lr
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
        pot_mob=potential_mobility(board,self.rules)
        n_stable=corner_stability(board,self.rules)
        n_corners=corner_count(board,self.rules)
        n_precorners=precorners_count(board,self.rules)

        features=np.zeros(self.dim)
        features[5*t:5*t+5]=np.array([mob,pot_mob,n_corners,n_precorners,n_stable])
        return features.reshape(1, -1)