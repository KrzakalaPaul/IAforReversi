
from arenas.game import game
from arenas.simulator import simulator,fight

from agents.all_agents import HumanAgent,RandomAgent,FullRandomMCTS


#fight(FullRandomMCTS(N_simulation=100),RandomAgent(),N=6,repeat=100,refresh_rate=10)

whiteplayer=HumanAgent()
blackplayer=FullRandomMCTS(simu_time=2)
game(whiteplayer,blackplayer,N=6)
