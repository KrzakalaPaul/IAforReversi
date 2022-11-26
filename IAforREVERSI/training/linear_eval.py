
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import os 
from reversi.heuristics import*
from reversi.rules import Rules
from training.data_set import DataSet_Games

import pickle

def sigmoid(x):
    return 1/(1 + np.exp(-x))


class LinearEvaluation():
    def  __init__(self,features_list):

        self.features_list=features_list
        self.dim=0
        for feature in features_list:
            self.dim+=feature.dim

        self.lr=LogisticRegression(fit_intercept=False,warm_start=True,max_iter=1000)
        self.lr.intercept_= np.zeros((1,))
        #self.lr.coef_= np.zeros((1,self.dim))
        self.lr.classes_=np.array([0,1])

        self.scaler=StandardScaler()
        #self.scaler.mean_=np.zeros((self.dim,))
        #self.scaler.var_=np.zeros((self.dim,))+1

        self.model= make_pipeline(StandardScaler(),self.lr)


    def feature_map(self,board):
        feats=[]
        for feature in self.features_list:
            feats+=feature(board)
        return np.array(feats)

    def fit(self,DSG):
        X,y=ConvertToDSF(DSG,self)
        self.model.fit(X=X,y=y)

    def __call__(self,board):
        feats=self.feature_map(board).reshape(1,-1)
        return self.model.predict_proba(feats)[0,1].item()  # type: ignore

    def format_path_save(self,name):
        update_counter=0
        folder_path = os.path.join(os.getcwd(), 'IAforREVERSI\\saves\\features')
        file_path=os.path.join(folder_path,name)

        if os.path.isfile(file_path):
            file_path=os.path.join(folder_path,name+f'_{update_counter}')
            while os.path.isfile(file_path):
                update_counter+=1
                file_path=os.path.join(folder_path,name+f'_{update_counter}')
        return file_path

    def format_path_load(self,name):
        folder_path = os.path.join(os.getcwd(), 'IAforREVERSI\\saves\\features')
        file_path=os.path.join(folder_path,name)
        return file_path
    
    def save(self,name):
        file_path=self.format_path_save(name)
        pickle.dump(self.model, open(file_path, 'wb'))
    
    def load(self,name):
        file_path=self.format_path_load(name)
        self.model=pickle.load(open(file_path, 'rb'))

    def print(self):
        print(self.lr.coef_)

from numpy.random import randint

def ConvertToDSF(DSG:DataSet_Games,eval:LinearEvaluation):
    N=DSG.N
    rules=Rules(N=N)
    d=eval.dim
    X=[]
    y=[]
    for game,results in zip(DSG.game_lists,DSG.results_list):
        board=rules.init_board()

        label=results
        if label==0.5:
            label=randint(2)
        label=int(label)

        for move in game[:-1]:
            X.append(eval.feature_map(board).reshape((1,-1)))
            y.append(label)
            rules.apply_move(board,move)
    X=np.concatenate(X)
    y=np.array(y)
    return X,y
        


class MyEval(LinearEvaluation):

    def  __init__(self,N):
        rules=Rules(N=N)
        super().__init__([mobility(rules),potential_mobility(rules),corner_count(rules),precorners_count(rules),corner_stability(rules)])



'''
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
'''