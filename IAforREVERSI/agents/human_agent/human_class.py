import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN
from agents.generic_agent import GenericAgent

class HumanAgent(GenericAgent):

    def ask_move(self,rules,board,displayer):
        wait_for_move = True
        while wait_for_move:
            for event in pg.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x=event.pos[0]
                    y=event.pos[1]
                    i,j=displayer.pixel_to_indices(x,y)
                    
                    if i in range(rules.N) and j in range(rules.N):
                        move=(i,j)
                        if rules.check_valid(board,move):
                            return move

            displayer.do_nothing()

                    
                    
 