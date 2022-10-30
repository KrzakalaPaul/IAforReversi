
### TRAINING AGENT :()

from reversi.heuristics import NaiveEval,Positions
from training.train_linear_eval import TrainLinearEvaluation

TrainLinearEvaluation(Positions())

### COMPETITION BETWEEN AGENTS : 

#from arenas.simulator import fight
#from agents.all_agents  import HumanAgent,RandomAgent,FullRandomMCTS,EvalMCTS
#from reversi.heuristics import NaiveEval,Positions

#agent1=FullRandomMCTS(simu_time=0.2,verbose=False)  # type: ignore
#agent1=EvalMCTS(NaiveEval(),simu_time=0.2,rollout_horizon=5, rollout_repeat=5,verbose=False)   # type: ignore
#agent2=EvalMCTS(Positions(N=6),simu_time=0.2,rollout_horizon=5, rollout_repeat=5,verbose=False)  # type: ignore
#fight(agent1,agent2,N=6,repeat=100,refresh_rate=10)  # type: ignore


### PLAYING THE GAME AGAINST AN AGENT : 

#from arenas.game import game
#agents.all_agents  import HumanAgent,RandomAgent,FullRandomMCTS,EvalMCTS

#whiteplayer=HumanAgent()
#blackplayer=FullRandomMCTS(simu_time=7)
#blackplayer=EvalMCTS(simu_time=2,rollout_horizon=0, rollout_repeat=1 ,verbose=True)
#game(whiteplayer,blackplayer,N=8)




