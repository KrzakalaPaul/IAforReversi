import pygame as pg
from pygame.locals import QUIT
from numpy import ndenumerate,copy

# Colors :

black_line= (0,0,0)
green_board = (30,80,40)
white_cirlce= (255,255,255)
black_cirlce = (0,0,0)
brown = (150,90,70)
red=(150,0,30)
blue=(60,70,200)


# Dimensions : 

size=600

offset=size/8
board_size=size-2*offset
line_width=size/100

class Displayer():

    def __init__(self,board):
        self.board=board
        self.fenetre=pg.display.set_mode((size, size))
        self.computing=False
        self.N=len(self.board.matrix)
        self.previous_matrix=copy(self.board.matrix)
        self.update()
        

    def add_board(self):
        
        N=self.N

        pg.draw.rect(self.fenetre, brown, pg.Rect(0, 0, size, size))
        pg.draw.rect(self.fenetre, green_board, pg.Rect(offset, offset, board_size, board_size))

        for k in range(N+1):
            pos=k*board_size/N+1
            pg.draw.rect(self.fenetre, black_line, pg.Rect(offset+pos-line_width/2, offset, line_width/2 , board_size))
            pg.draw.rect(self.fenetre, black_line, pg.Rect(offset, offset+pos-line_width/2, board_size , line_width/2))

        pg.draw.circle(self.fenetre, black_line, (offset+board_size*2/N, offset+board_size*2/N), 2*line_width)
        pg.draw.circle(self.fenetre, black_line, (offset+board_size-board_size*2/N, offset+board_size-board_size*2/N), 2*line_width)
        pg.draw.circle(self.fenetre, black_line, (offset+board_size-board_size*2/N, offset+board_size*2/N), 2*line_width)
        pg.draw.circle(self.fenetre, black_line, (offset+board_size*2/N, offset+board_size-board_size*2/N), 2*line_width)
        
        circle_radius=0.9*board_size/(self.N)
        y=offset/2
        x=size/2
        if self.board.current_color=='White':
            pg.draw.circle(self.fenetre, white_cirlce, (x, y), circle_radius/2)
        if self.board.current_color=='Black':
            pg.draw.circle(self.fenetre, black_cirlce, (x, y), circle_radius/2)

        pg.display.flip()

    def pixel_to_indices(self,x,y):
        i=(x-offset)//(board_size/self.N)
        j=(y-offset)//(board_size/self.N)
        return int(i),int(j)

    def indices_to_pixel(self,i,j):
        x=offset+(i+0.5)*board_size/self.N
        y=offset+(j+0.5)*board_size/self.N
        return x,y

    def update(self):
        new_matrix=self.board.matrix

        self.add_board()

        circle_radius=0.9*board_size/(self.N)

        for (i,j),value in ndenumerate(new_matrix):
                x,y=self.indices_to_pixel(i,j)
                if value==1:
                    pg.draw.circle(self.fenetre, white_cirlce, (x, y), circle_radius/2)
                elif value==-1:
                    pg.draw.circle(self.fenetre, black_cirlce, (x, y), circle_radius/2)

                old_value=self.previous_matrix[i,j]
                if value!=old_value:
                    if old_value==0:
                        pg.draw.circle(self.fenetre, blue, (x, y), circle_radius/10)
                    else:
                        pg.draw.circle(self.fenetre, red, (x, y), circle_radius/10)
        self.previous_matrix=copy(new_matrix)


        pg.display.flip()

    def wait(self):
        wait=True
        while wait:
            for event in pg.event.get():   #On parcours la liste de tous les événements reçus
                if event.type == QUIT:     #Si un de ces événements est de type QUIT
                    wait = False

    def do_nothing(self):
        pg.event.pump()
