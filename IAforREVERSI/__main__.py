
### PRECOMPUTING DATA SETS:

"""
from training.data_set import CreateDataSet,LoadDataSet
from agents.all_agents  import HumanAgent,RandomAgent,FullRandomMCTS,EvalMCTS
CreateDataSet('MCTS_t3_dataset_2',FullRandomMCTS(simu_time=3,verbose=False),FullRandomMCTS(simu_time=3,verbose=False),n_game=100,N=8)
data_board,data_label=LoadDataSet('test_dataset')
"""

### TRAINING AGENT :
"""
from reversi.heuristics import NaiveEval,Positions,StabilityAndMobility
from training.train_linear_eval import TrainLinearEvaluation


# Using Precomputed dataset for first step :
N=8
t=1
TrainLinearEvaluation(StabilityAndMobility(N=N),H=6,k=5,t=t,n_eval=100,n_update=0,save=None,precomputed_data_set='MCTS_t3_dataset')
"""

### COMPETITION BETWEEN AGENTS : 

from tabnanny import verbose
from arenas.simulator import fight
from agents.all_agents  import HumanAgent,RandomAgent,FullRandomMCTS,EvalMCTS
from reversi.heuristics import NaiveEval,Positions,StabilityAndMobility

#agent1=FullRandomMCTS(simu_time=1,verbose=False)  # type: ignore

eval_fct1=StabilityAndMobility(N=8,save='D:\\Documents\\AAA\\IAforReversi\\IAforREVERSI\\saves\\StabilityAndMobility-RandomData\\coef.npy')
agent1=EvalMCTS(eval_fct1,simu_time=0.5,rollout_horizon=5, rollout_repeat=3 ,verbose=False)

eval_fct2=StabilityAndMobility(N=8,save='D:\\Documents\\AAA\\IAforReversi\\IAforREVERSI\\saves\\StabilityAndMobility-MCTS-3\\coef.npy')
agent2=EvalMCTS(eval_fct2,simu_time=0.5,rollout_horizon=5, rollout_repeat=3 ,verbose=False)

fight(agent1,agent2,N=8,repeat=100,refresh_rate=10)  # type: ignore

### PLAYING THE GAME AGAINST AN AGENT : 

"""
from arenas.game import game
from agents.all_agents  import HumanAgent,RandomAgent,FullRandomMCTS,EvalMCTS
from reversi.heuristics import NaiveEval,Positions,StabilityAndMobility

whiteplayer=HumanAgent()
#blackplayer=FullRandomMCTS(simu_time=2,verbose=True)

eval_fct=StabilityAndMobility(N=8,save='D:\\Documents\\AAA\\IAforReversi\\IAforREVERSI\\saves\\StabilityAndMobility-RandomData\\coef.npy')
blackplayer=EvalMCTS(eval_fct,simu_time=5,rollout_horizon=0, rollout_repeat=1 ,verbose=True)

game(whiteplayer,blackplayer,N=8)
"""