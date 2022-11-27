from random import choice
from numpy.random import random
import numpy as np
from agents.generic_agent import GenericAgent
from reversi.board import Board
from reversi.rules import Rules

class GreedyAgent(GenericAgent):

    def __init__(self,eval,eps=None):
        self.eval=eval
        self.eps=eps

    def ask_move(self,rules:Rules,board:Board,displayer):
        
        if self.eps!=None:
            if random()<self.eps:
                return choice(board.valid_moves)

        if board.current_color=='White':
            team=1
        else:
            team=-1

        values=[]
        for move in board.valid_moves:
            new_board=board.copy()
            rules.apply_move(new_board,move)

            if new_board.current_color==None:
                values.append(rules.white_win(new_board))
            else:
                values.append(self.eval(new_board))

        return board.valid_moves[np.argmax(team*np.array(values))]