from agents.generic_agent import GenericAgent
from numpy import array,argmax, isin

class Node():
    def __init__(self):
        self.reward_sum=0
        self.n_simu=0
        self.children=[]
        self.moves=[]
        self.team=None
        self.parent=None

    def white_score(self):
        if self.team=='White':
            return self.reward_sum/self.n_simu

        if self.team=='Black':
            return 1-self.reward_sum/self.n_simu


class TerminalNode():
    def __init__(self):
        self.white_win=0
        self.parent=Node()

    def white_score(self):
        return self.white_win




class GenericMCTS(GenericAgent):

    def __init__(self,N_simulation=100):
        self.N_simulation=N_simulation 

    def new_game(self,starting_board,rules):
        self.rules=rules
        self.true_board=starting_board.copy()

        self.root=Node()
        self.root.team=starting_board.current_color

    def observe_move(self,new_move):

        self.rules.apply_move(self.true_board,new_move)

        # Check if the move is known
        for k,move in enumerate(self.root.moves):
            if move==new_move:
                self.root=self.root.children[k]
                return

        # Else create new tree
        self.root=Node()
        self.root.team=self.true_board.current_color

    def select_child(self,node):
        return 0
    
    def expand(self,node,board):
        
        for legal_move in self.rules.list_valid_moves(board):
            new_node=Node()
            new_node.parent=node
            node.moves.append(legal_move)
            node.children.append(new_node)

    def eval(self,board_to_eval):
        return 1,0

    def backprop(self,child):

        if isinstance(child,TerminalNode):
            ancester=child.parent
            while ancester!=None:

                ancester.n_simu+=1
                if ancester.team=='White':
                    ancester.reward_sum+=child.white_win
                else:
                    ancester.reward_sum+=1-child.white_win

                ancester=ancester.parent

        else:
            value=child.reward_sum/child.n_simu

            ancester=child.parent
            while ancester!=None:
                ancester.n_simu+=1
                if ancester.team==child.team:
                    ancester.reward_sum+=value
                else:
                    ancester.reward_sum+=1-value
                ancester=ancester.parent
                


    def simulation(self):

        # New Simulation 
        board_simulation=self.true_board.copy()
        current_node=self.root

        # Selection Part 

        while len(current_node.children)==[]: 

            k=self.select_child(current_node)
            
            move=current_node.moves[k]
            self.rules.apply_move(board_simulation,move)

            current_node=current_node.children[k]
        
        if isinstance(current_node,TerminalNode):
            self.backprop(current_node)

        else:
            # Expansion
            self.expand(current_node,board_simulation)

            # Evaluation
            for k,child in enumerate(current_node.children):

                board_to_eval=board_simulation.copy()
                self.rules.apply_move(board_to_eval,current_node.moves[k])
                child.team=board_to_eval.current_color

                if child.team==None: # Terminal State !
                    current_node.children[k]=TerminalNode()
                    current_node.children[k].white_win=self.rules.white_win(board_to_eval)

                else:
                    n_simu,value=self.eval(board_to_eval)
                    child.n_simu=n_simu
                    child.reward_sum=value


            # Backprop
            for child in current_node.children:
                self.backprop(child)  



    def ask_move(self,rules,board,displayer):
        
        for _ in range(self.N_simulation):  # Can add a command to stop simulation here
            self.simulation()
        
        if board.current_color=='White':
            greedy_score=[child.white_score()  for child in self.root.children]
        else:
            greedy_score=[1-child.white_score()  for child in self.root.children]

        choice=argmax(array(greedy_score))
        return self.root.moves[choice]
            