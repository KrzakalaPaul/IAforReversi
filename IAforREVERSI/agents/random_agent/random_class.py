from random import choice
from agents.generic_agent import GenericAgent

class RandomAgent(GenericAgent):

    def ask_move(self,rules,board,displayer):
        List=rules.list_valid_moves(board)
        return choice(List)