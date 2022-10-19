
from arenas.game import game
from arenas.simulator import simulator

from agents.all_agents import HumanAgent,RandomAgent

player1=HumanAgent()
player2=RandomAgent()

game(player1,player2)

