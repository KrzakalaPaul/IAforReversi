
from agents.all_agents  import RandomAgent,FullRandomMCTS,EvalMCTS,GreedyAgent

### Test time complexity
"""
from Test.time_complexity import heuristics,moves
moves()
heuristics()

"""
### Plot Time vs Winrate
"""
from arenas.plot import time_plot
import numpy as np
time_plot(N=6,T=[1e-3,5*1e-3,1e-2,5*1e-2,1e-1])

"""

### LOADING AGENT :
"""
agent1=FullRandomMCTS(simu_time=0.5,verbose=True)    # type: ignore
agent2=FullRandomMCTS(simu_time=0.5,verbose=True) 

from training.data_set import generate_DSG,load_DSG
from training.linear_eval import MyEval



DSG=load_DSG('MCTS_simu5_selfplayx200',N=8)
eval_svm=MyEval(N=8,t_augmentation=4,model_choice='SVM')
eval_svm.fit(DSG)
eval_svm.save('eval_svm')
eval_svm.load('eval_svm')
agent_svm=EvalMCTS(eval_svm,simu_time=3,c=1,n_simu_init=2, rollout_horizon=0, rollout_repeat=1 ,verbose=True)

eval_logistic=MyEval(N=8,t_augmentation=4,model_choice='Logistic')
eval_logistic.fit(DSG)
eval_logistic.save('eval_Logistic')
eval_logistic.load('eval_Logistic')
agent_logitsic=EvalMCTS(eval_logistic,simu_time=3,c=1,n_simu_init=2, rollout_horizon=0, rollout_repeat=1 ,verbose=True)
"""
### TRAINING AGENT :

from training.data_set import generate_DSG,load_DSG
from training.linear_eval import MyEval
from training.train_greedy_iter import train_greedy
from training.train_MCTS_iter import train_MCTS

'''  
N=8
eval1=MyEval(N=N,t_augmentation=4)
#train_greedy(eval1,N=N,N_outer=10,N_games=100,eps=0.01)
#eval.save('10x100_eps0.01_six4_N8')
eval1.load('10x100_eps0.01_six4_N8')
agent1=GreedyAgent(eval1)
'''  

N=6
eval=MyEval(N=N,t_augmentation=4,model_choice='SVM')
train_MCTS(eval,N=N,N_outer=5,N_games=100,simu_time=1,save_name='TestN6_SVM') # type: ignore

### Create DataSets
'''
agent1=FullRandomMCTS(simu_time=10,verbose=False)   
agent2=FullRandomMCTS(simu_time=10,verbose=False) 

DSG=generate_DSG(agent1,agent2,N=8,N_games=200)
DSG.save('MCTS_simu5_selfplayx100')  
'''
### COMPETITION BETWEEN AGENTS : 
'''
from arenas.simulator import fight
from time import time

fight(agent1,agent2,N=8,repeat=100,refresh_rate=10)  # type: ignore
'''
### PLAYING THE GAME AGAINST AN AGENT : 
'''
from arenas.game import game
from agents.all_agents  import HumanAgent


#whiteplayer=RandomAgent()
#blackplayer=HumanAgent()

whiteplayer=agent1
blackplayer=agent2

game(whiteplayer,blackplayer,N=6)
'''