class Board():
    def __init__(self,matrix,current_color):
        self.matrix=matrix
        self.current_color=current_color
        self.valid_moves=[]
        self.frontier='Uncomputed'

    def copy(self):
        board_copy=Board(self.matrix.copy(),self.current_color)
        board_copy.valid_moves=self.valid_moves.copy()
        board_copy.frontier=self.frontier.copy()
        return board_copy