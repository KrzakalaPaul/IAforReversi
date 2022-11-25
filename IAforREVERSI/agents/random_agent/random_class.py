from random import choice
from agents.generic_agent import GenericAgent

class RandomAgent(GenericAgent):

    def ask_move(self,rules,board,displayer):
        List=board.valid_moves
        return choice(List)