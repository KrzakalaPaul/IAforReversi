class Node():
    def __init__(self):
        self.reward_sum=0
        self.n_simu=0
        self.children=[]
        self.moves=[]
        self.team=None
        self.parent=None


class Tree():
    def __init__(self):
        self.root=None