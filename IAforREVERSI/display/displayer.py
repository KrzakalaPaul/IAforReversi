import pygame as pg
pg.init()
#from pygame.locals import *

class Displayer():

    def __init__(self,board):
        self.board=board
        self.fenetre=pg.display.set_mode((640, 480))
        self.computing=False
        self.update()


    def update(self):
        pg.display.flip()





