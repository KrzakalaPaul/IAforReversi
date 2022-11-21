
from agents.all_agents  import RandomAgent,FullRandomMCTS,EvalMCTS
from reversi.heuristics import NaiveEval,Positions,Three,Four,Five

### LOADING AGENT :

#agent1=FullRandomMCTS(simu_time=3,verbose=False)
#agent2=FullRandomMCTS(simu_time=1)

eval_fct1=Five(N=8,save='D:\\Documents\\AAA\\IAforReversi\\IAforREVERSI\\saves\\Five_run_0\\coef_8',scaling=True)
agent1=EvalMCTS(eval_fct1,simu_time=7,rollout_horizon=0, rollout_repeat=1 ,verbose=False)  # type: ignore

#eval_fct2=Five(N=8,save='D:\\Documents\\AAA\\IAforReversi\\IAforREVERSI\\saves\\Five_run_0\\coef_8',scaling=True)
#agent2=EvalMCTS(eval_fct2,simu_time=7,rollout_horizon=0, rollout_repeat=1 ,verbose=False)  # type: ignore

#agent2=FullRandomMCTS(simu_time=1,verbose=False)  # type: ignore


### PRECOMPUTING DATA SETS:
"""
from training.data_set import CreateDataSet,LoadDataSet,UnionDataSet

#from time import time
#t=time()
#winrate_1=CreateDataSet('test',RandomAgent(),RandomAgent(),n_game=1000,N=8)
#print(time()-t)

#UnionDataSet(['data_0','data_1','data_2','data_3'],'FiveNoScalingTraining')
"""
### TRAINING AGENT :
"""
from training.train_linear_eval import TrainLinearEvaluation

N=8    
t=3
eval_to_train=Five(game_states=3,N=8,scaling=True)

TrainLinearEvaluation(eval_to_train,H=0,k=1,t=t,n_eval=100,n_update=10,save=None,precomputed_data_set=None)

# Using Precomputed dataset for first step :
#TrainLinearEvaluation(eval_to_train,H=0,k=1,t=t,n_eval=100,n_update=0,save=None,precomputed_data_set='All')
"""
### COMPETITION BETWEEN AGENTS : 
"""
from arenas.simulator import fight
from time import time

fight(agent1,agent2,N=8,repeat=100,refresh_rate=10)  # type: ignore
"""
### PLAYING THE GAME AGAINST AN AGENT : 

from arenas.game import game
from agents.all_agents  import HumanAgent

whiteplayer=agent1

blackplayer=HumanAgent()
#blackplayer=agent2

game(whiteplayer,blackplayer,N=8)
