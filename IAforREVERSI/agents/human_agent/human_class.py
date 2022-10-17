import pygame as pg
from pygame.locals import MOUSEBUTTONDOWN
pg.init()

class HumanAgent():
    def __init__(self):
        pass 

    def ask_move(self,rules,board,displayer):
        wait_for_move = True
        while wait_for_move:
            for event in pg.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Convert event.pos into move using Rules.N et displayer.size
                    return None
 