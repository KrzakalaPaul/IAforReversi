
from agents.all_agents  import RandomAgent,FullRandomMCTS,EvalMCTS

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

# Create Data set
from training.data_set import generate_DSG,merge_from_name

merge_from_name('random_games',"random_games",'random_gamesx2')



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

#whiteplayer=agent1
whiteplayer=RandomAgent()
blackplayer=HumanAgent()

game(whiteplayer,blackplayer,N=6)
"""