
from arenas.game import game
from arenas.simulator import simulator,fight
from arenas.plot import Plot
from agents.all_agents  import HumanAgent,RandomAgent,FullRandomMCTS,EvalMCTS
from reversi.heuristics import NaiveEval,Positions

#Plot()

#agent1=FullRandomMCTS(simu_time=0.2,verbose=False)  # type: ignore
agent1=EvalMCTS(simu_time=0.2,rollout_horizon=5, rollout_repeat=5,eval_fct=NaiveEval(),verbose=False)   # type: ignore
agent2=EvalMCTS(simu_time=0.2,rollout_horizon=5, rollout_repeat=5,eval_fct=Positions(N=6),verbose=False)  # type: ignore
fight(agent1,agent2,N=6,repeat=100,refresh_rate=10)  # type: ignore

#whiteplayer=HumanAgent()
#blackplayer=FullRandomMCTS(simu_time=7)
#blackplayer=EvalMCTS(simu_time=2,rollout_horizon=0, rollout_repeat=1 ,verbose=True)
#game(whiteplayer,blackplayer,N=8)




