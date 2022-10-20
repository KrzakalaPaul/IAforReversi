from agents.generic_agent import GenericAgent
from numpy import array,argmax
from time import time 

class Node():
    def __init__(self):
        self.reward_sum=0.0
        self.n_simu=0
        self.children=[]
        self.moves=[]
        self.team=None
        self.parent=None

    def white_score(self):
        if self.n_simu==0:
            return 0.5

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

    def winner(self):
        if self.white_win==1:
            return 'White'
        else:
            return 'Black'



class GenericMCTS(GenericAgent):

    def __init__(self,simu_time=1,verbose=True):
        self.simu_time=simu_time
        self.verbose=verbose
        self.tree_depth=0

    def new_game(self,starting_board,rules):
        self.rules=rules
        self.true_board=starting_board.copy()

        self.root=Node()
        self.root.n_simu=1
        self.root.reward_sum=0.5
        self.root.team=starting_board.current_color

    def observe_move(self,new_move):

        self.rules.apply_move(self.true_board,new_move)

        # Check if the move is known
        for k,move in enumerate(self.root.moves):
            if move==new_move:
                self.root=self.root.children[k]
                self.tree_depth=self.tree_depth=-1
                print('move already explored')
                return

        # Else create new tree
        self.root=Node()
        self.root.n_simu=1
        self.root.reward_sum=0.5
        self.root.team=self.true_board.current_color
        self.tree_depth=0

    def select_child(self,node):
        return 0
    
    def expand(self,node,board):
        
        for legal_move in self.rules.list_valid_moves(board):
            
            # Check For Terminal Node :
            board_after_move=board.copy()
            self.rules.apply_move(board_after_move,legal_move)
            terminal=(board_after_move.current_color==None)

            if terminal:
                new_node=TerminalNode()
                new_node.parent=node
                new_node.white_win=self.rules.white_win(board_after_move)
                node.moves.append(legal_move)
                node.children.append(new_node)

            else:
                new_node=Node()
                new_node.parent=node
                new_node.team=board_after_move.current_color
                node.moves.append(legal_move)
                node.children.append(new_node)



    def eval(self,board_to_eval): # Eval position (return value)
        return 0

    def eval_children(self,current_node,board_simulation): # Eval some of the child node (return list of evaluated)
        return []


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
        depth=0

        stopping_condition=(len(current_node.children)==0) 
        assert isinstance(current_node,Node)
        while not(stopping_condition):

            k=self.select_child(current_node)
            
            move=current_node.moves[k]  # type: ignore
            self.rules.apply_move(board_simulation,move)

            current_node=current_node.children[k]  # type: ignore

            stopping_condition=isinstance(current_node,TerminalNode) or len(current_node.children)==0 or current_node.n_simu==0

            depth+=1

        self.tree_depth=max(self.tree_depth,depth)

        if isinstance(current_node,TerminalNode):
                self.backprop(current_node)

        elif current_node.n_simu==0:  # type: ignore
            reward=self.eval(board_simulation)
            current_node.n_simu=1  # type: ignore
            current_node.reward_sum=reward  # type: ignore
            self.backprop(current_node)

        else:
            # Expansion
            self.expand(current_node,board_simulation)

            # Evaluation
            evaluated_child=self.eval_children(current_node,board_simulation)

            # Backprop
            for k in evaluated_child:
                self.backprop(current_node.children[k])  



    def ask_move(self,rules,board,displayer):
        start_simu_time=time()
        N_simu=0
        while time()-start_simu_time<self.simu_time:
            self.simulation()
            N_simu+=1
        if self.verbose:
            print(f"Nombre simulation {N_simu}")
            print(f"Simulation/Seconde {N_simu/self.simu_time}")
            print(f"Tree depth : {self.tree_depth}")
        
        if board.current_color=='White':
            greedy_score=[child.white_score()  for child in self.root.children]
        else:
            greedy_score=[1-child.white_score()  for child in self.root.children]

        choice=argmax(array(greedy_score))
        return self.root.moves[choice]
            