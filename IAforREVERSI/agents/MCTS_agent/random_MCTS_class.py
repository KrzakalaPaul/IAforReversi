from IAforREVERSI.reversi.rules import Rules
from agents.MCTS_agent.tree import Node
from agents.generic_agent import GenericAgent
from numpy import array,argmax

class RandomMCTSAgent(GenericAgent):

    def __init__(self,N_simulation=1000):
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

    def select(self,children):
        return 0
    
    def expand(self,node,board):

        for legal_move in self.rules.list_valid_moves(board):
            node.moves.append(legal_move)
            new_node=Node()
            new_node.parent=node
            node.children.append(new_node)

    def eval(self,board_to_eval):
        return 0


    def simulation(self):

        # New Simulation 
        board_simulation=self.true_board.copy()
        current_node=self.root

        # Selection Part 
        while current_node.children!=[]:
            
            k=self.select(current_node.children)
            
            current_node=current_node.children[k]

            move=current_node.moves[k]
            self.rules.apply_move(board_simulation,move)

        # Expansion
        self.expand(current_node,board_simulation)

        # Evaluation
        for k,child in enumerate(current_node.children):
            board_to_eval=board_simulation.copy()
            rules.apply_move(board_to_eval,current_node.moves[k])
            child.team=board_to_eval.current_color

            value=self.eval(board_to_eval)
            child.n_simu=1
            child.reward_sum=value

        def ask_move(self,rules,board,displayer):
            
            for _ in range(self.N_simulation):  # Can add a command to stop simulation here
                self.explore_tree()

            greedy_reward=[child.reward_sum/child.n_simu  for child in self.root.children]
            choice=argmax(array(greedy_reward))

            return self.root.moves[choice]
                


        









