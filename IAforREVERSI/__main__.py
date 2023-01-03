
### Test time complexity
"""
from Test.time_complexity import heuristics,moves
moves()
heuristics()
"""

### TRAINING AGENT :
"""
from training.data_set import generate_DSG,load_DSG
from training.linear_eval import MyEval
from training.train_greedy_iter import train_greedy
from training.train_MCTS_iter import train_MCTS


# Training with MCTS iteration
N=8
eval=MyEval(N=N,t_augmentation=5,model_choice='Logistic',C=1e-3)
train_MCTS(eval,N=N,N_outer=10,N_games=200,simu_time=5,save_name='final_run') # type: ignore
#eval.save('MCTS_trained_eval')

# Training with eps-Greedy agent (Temporal Difference)
N=8
eval=MyEval(N=N,t_augmentation=5,model_choice='Logistic',C=1e-3)
train_greedy(eval1,N=N,N_outer=10,N_games=100,eps=0.01)
#eval.save('TD_trained_eval')
"""

### LOADING AGENT :

from agents.all_agents  import RandomAgent,FullRandomMCTS,EvalMCTS,GreedyAgent
from training.linear_eval import MyEval
t=10

# Vanilla MCTS:
agent_MCTS=FullRandomMCTS(simu_time=t,verbose=False,children_init='one')    # type: ignore

eval=MyEval(N=8,t_augmentation=5,model_choice='Logistic',C=1e-3)
eval.load('default')

# Augmented MCTS:
agent_augmented_MCTS=EvalMCTS(eval,simu_time=t,c=1,n_simu_init=2, rollout_horizon=0, rollout_repeat=1 ,verbose=True)

# Greedy:
agent_greedy=GreedyAgent(eval)

# Greedy Rollouts MCTS:
def give_agent():
    return GreedyAgent(eval)
agent_greedyrollouts_MCTS=FullRandomMCTS(simu_time=t,verbose=False,children_init='one',rollout_agent=give_agent)

# Random Agent:
agent_random=RandomAgent()

### Plots :

"""
# Final Competition between the agents
from arenas.plot import competition
competition(agents_list=[agent_random,agent_greedy,agent_MCTS,agent_greedyrollouts_MCTS,agent_augmented_MCTS],n_games=10,N=8)

# Plots winrate vs time and winrate vs C
from arenas.plot import time_plot,c_plot
import numpy as np
T=np.array([1e-3,5*1e-3,7*1e-3,1e-2,2*1e-2,5*1e-2,1e-1])
time_plot(N=6,T=T)
c_plot(N=6,C=np.array([0.001,0.01,0.1,1,10,100,1000]),t=1e-2)
"""


### PLAYING THE GAME AGAINST AN AGENT : 

from arenas.game import game
from agents.all_agents  import HumanAgent

whiteplayer=HumanAgent()
#whiteplayer=agent_MCTS
blackplayer=agent_augmented_MCTS

game(whiteplayer,blackplayer,N=8)
