import json
import os 
from arenas.simulator import simulator_with_save
from reversi.rules import Rules
import numpy as np

###----------------------- Data Set of GAMES (as sequences of moves) ----------------------- ###

# Class :

class DataSet_Games():
    def __init__(self,N):
        self.N=N
        self.game_lists=[]
        self.results_list=[]
    
    def add(self,game,result):
        self.game_lists.append(game)
        self.results_list.append(result)

    def save(self,name='unnamed_DSG'):
        file_path=self.format_path_save(name)
        dic={'games':self.game_lists,'results':self.results_list}
        with open(file_path, 'w') as f:
            json.dump(dic,f)
    
    def load(self,name='unnamed_DSG'):
        file_path=self.format_path_load(name)

        with open(file_path) as f:
            dic = json.load(f)
        self.game_lists=dic['games']
        self.results_list=dic['results']

    def format_path_save(self,name):
        update_counter=0
        folder_path = os.path.join(os.getcwd(), 'IAforREVERSI\\saves\\datasets')
        file_path=os.path.join(folder_path,name+'.json')

        if os.path.isfile(file_path):
            file_path=os.path.join(folder_path,name+f'_{update_counter}.json')
            while os.path.isfile(file_path):
                update_counter+=1
                file_path=os.path.join(folder_path,name+f'_{update_counter}.json')
        return file_path

    def format_path_load(self,name):
        folder_path = os.path.join(os.getcwd(), 'IAforREVERSI\\saves\\datasets')
        file_path=os.path.join(folder_path,name+'.json')
        return file_path


# Associated Functions:

def load_DSG(name,N):
    DSG=DataSet_Games(N=N)
    DSG.load(name)
    return DSG


def generate_DSG(Agent1,Agent2,N,N_games,verbose=False,random_moves=2):

    DSG=DataSet_Games(N)
    
    wins_Agent1=0
    k=0

    for _ in range(N_games//2):
        white_agent=Agent1
        black_agent=Agent2
        winner,game=simulator_with_save(white_agent,black_agent,N=N,random_moves=random_moves)
        wins_Agent1+=winner
        DSG.add(game,winner)
        k+=1
        if verbose:
            print(f'{int(100*k/N_games)}%')

    for _ in range(N_games//2):
        white_agent=Agent2
        black_agent=Agent1
        winner,game=simulator_with_save(white_agent,black_agent,N=N,random_moves=random_moves)
        wins_Agent1+=1-winner
        DSG.add(game,winner)
        k+=1
        if verbose:
            print(f'{int(100*k/N_games)}%')

    return DSG,wins_Agent1/k

def merge_DSG(DSG1:DataSet_Games,DSG2:DataSet_Games):
    assert DSG1.N==DSG2.N
    DSG=DataSet_Games(DSG1.N)

    for game,result in zip(DSG2.game_lists,DSG2.results_list):
        DSG.add(game,result)

    for game,result in zip(DSG2.game_lists,DSG2.results_list):
        DSG.add(game,result)

    return DSG

def merge_DSG_list(List):
    DSG=List[0]
    for new_DSG in List[1:]:
        DSG=merge_DSG(DSG,new_DSG)
    return DSG

    
def merge_from_name(name1,name2,newname,N=8):
    DSG1=DataSet_Games(N)
    DSG1.load(name1)
    DSG2=DataSet_Games(N)
    DSG2.load(name2)
    DSG=merge_DSG(DSG1,DSG2)
    DSG.save(newname)


