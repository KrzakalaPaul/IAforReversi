
import numpy as np
np.set_printoptions(precision=2)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
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
    def  __init__(self,features_list,t_augmentation,model_choice='Logistic'):

        self.features_list=features_list
        self.nat_dim=0
        for feature in features_list:
            self.nat_dim+=feature.dim
        self.dim=self.nat_dim*t_augmentation
        N=features_list[0].rules.N
        self.time_codes=np.linspace(0,N**2,t_augmentation+1)

        if model_choice=='Logistic':
            self.model_choice=model_choice
            self.lr=LogisticRegression(fit_intercept=False,warm_start=True,max_iter=1000)
            self.lr.intercept_= np.zeros((1,))
            self.lr.classes_=np.array([0,1])
        elif model_choice=='SVM':
            self.model_choice=model_choice
            self.lr=SVC(gamma='scale',probability=True)
        
        self.scaler=StandardScaler(with_mean=False)
        self.model= make_pipeline(self.scaler,self.lr)
        #self.model= self.lr

    def feature_map(self,board):

        n_moves=np.sum(np.abs(board.matrix))
        # Looking for time_code : 
        t=0
        while n_moves>self.time_codes[t+1]:
            t+=1

        feats=[]
        for feature in self.features_list:
            feats+=feature(board)
        feats=np.array(feats)

        augmented_feats=np.zeros(self.dim)
        augmented_feats[self.nat_dim*t:self.nat_dim*t+self.nat_dim]=feats

        return augmented_feats

    def fit(self,DSG):
        X,y=ConvertToDSF(DSG,self)
        self.model.fit(X=X,y=y)
        print(f'Score: {self.model.score(X=X,y=y)}')

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

        if self.model_choice=='Logistic':
        
            for t in range(len(self.time_codes)-1):
                
                var=self.scaler.var_[self.nat_dim*t:self.nat_dim*t+self.nat_dim]  # type: ignore
                coefs=self.lr.coef_[0,self.nat_dim*t:self.nat_dim*t+self.nat_dim]

                print(f'Turns {int(self.time_codes[t])} to {int(self.time_codes[t+1])}...')
                print(f'var: {var}')
                print(f'coefs: {coefs}')

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
            move=tuple(move)
            X.append(eval.feature_map(board).reshape((1,-1)))
            y.append(label)
            rules.apply_move(board,move)
    X=np.concatenate(X)
    y=np.array(y)
    return X,y
        


class MyEval(LinearEvaluation):

    def  __init__(self,N,t_augmentation=3,model_choice='Logistic'):
        rules=Rules(N=N)
        super().__init__([corner_count(rules),mobility(rules),potential_mobility(rules),corner_stability(rules),naive(rules),precorners_count(rules),skiped(rules)],t_augmentation=t_augmentation,model_choice=model_choice)




