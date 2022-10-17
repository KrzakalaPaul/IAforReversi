from torch import arange
from IAforREVERSI.arenas.game import game
from IAforREVERSI.arenas.simulator import simulator

from IAforREVERSI.agents.human_agent.human_class import HumanAgent
from IAforREVERSI.agents.random_agent.random_class import RandomAgent

player1=HumanAgent()
player2=RandomAgent()

game(player1,player2)
