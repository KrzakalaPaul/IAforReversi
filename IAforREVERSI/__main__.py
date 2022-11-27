
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
agent1=FullRandomMCTS(simu_time=0.1,verbose=True)    # type: ignore
agent2=FullRandomMCTS(simu_time=1,verbose=True) 
"""
### TRAINING AGENT :

from training.data_set import generate_DSG,load_DSG
from training.linear_eval import MyEval
from training.train_greedy_iter import train_greedy

'''
N=8 
eval=MyEval(N=N,t_augmentation=3)
train_greedy(eval,N=N,N_outer=10,N_games=500,eps=0.05,verbose=True)
'''
  
'''
N=8
eval1=MyEval(N=N,t_augmentation=4)
#train_greedy(eval1,N=N,N_outer=10,N_games=100,eps=0.01)
#eval.save('10x100_eps0.01_six4_N8')
eval1.load('10x100_eps0.01_six4_N8')
agent1=GreedyAgent(eval1)

DSG=load_DSG('100RandomGames_N8',N=8)
eval2=MyEval(N=N,t_augmentation=4)
#eval2.fit(DSG)
#eval2.save('100RandomGames_six4_N8')
eval2.load('100RandomGames_six4_N8')
agent2=GreedyAgent(eval2)
'''
### Create DataSets

agent1=FullRandomMCTS(simu_time=5,verbose=False)   
agent2=FullRandomMCTS(simu_time=5,verbose=False) 

DSG=generate_DSG(agent1,agent2,N=8,N_games=100)
DSG.save('MCTS_simu5_selfplayx100')

### COMPETITION BETWEEN AGENTS : 
"""
from arenas.simulator import fight
from time import time

fight(agent1,agent2,N=8,repeat=100,refresh_rate=10)  # type: ignore
"""
### PLAYING THE GAME AGAINST AN AGENT : 
"""
from arenas.game import game
from agents.all_agents  import HumanAgent


#whiteplayer=RandomAgent()
#blackplayer=HumanAgent()

whiteplayer=agent2
blackplayer=agent1

game(whiteplayer,blackplayer,N=8)
"""