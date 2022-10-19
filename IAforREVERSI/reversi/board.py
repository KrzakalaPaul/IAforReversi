class Board():
    def __init__(self,matrix,current_color):
        self.matrix=matrix
        self.current_color=current_color

    def copy(self):
        return Board(self.matrix.copy(),self.current_color)