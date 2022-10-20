
from arenas.game import game
from arenas.simulator import simulator,fight
from arenas.plot import Plot
from agents.all_agents  import HumanAgent,RandomAgent,FullRandomMCTS


#Plot()

#fight(FullRandomMCTS(simu_time=0.2,verbose=False),RandomAgent(),N=4,repeat=100,refresh_rate=10)  # type: ignore

whiteplayer=HumanAgent()
blackplayer=FullRandomMCTS(simu_time=7)
game(whiteplayer,blackplayer,N=8)




