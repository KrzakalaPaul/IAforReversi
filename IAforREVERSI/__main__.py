
from arenas.game import game
from arenas.simulator import simulator,fight

from agents.all_agents import HumanAgent,RandomAgent,FullRandomMCTS


#fight(FullRandomMCTS(N_simulation=1,N_rollout=1),RandomAgent(),N=4,repeat=1000,refresh_rate=10)

whiteplayer=HumanAgent()
blackplayer=FullRandomMCTS(N_simulation=1000,N_rollout=100)
game(whiteplayer,blackplayer,N=8)

