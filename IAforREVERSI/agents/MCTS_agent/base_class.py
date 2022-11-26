from agents.generic_agent import GenericAgent
from numpy import array,argmax,allclose
from time import time 
from numpy import inf

class Root():   
    def __init__(self,board):
        self.score_sum=0.0
        self.n_simu=0
        self.children=[]
        if board.current_color=='White':
            self.team=1
        else:
            self.team=-1
        self.board=board
        self.solved=False
        self.exact_score=None

class Leaf():   
    def __init__(self):
        self.temporary_score=0.0
        self.move=None
        self.team=None
        self.parent=None
        self.board=None

    def score(self):
        return self.temporary_score
    
    def ucb_score(self):
        return self.temporary_score

class Node():
    def __init__(self,ex_leaf):

        self.score_sum=0
        self.n_simu=0

        self.solved=False
        self.exact_score=None

        self.move=ex_leaf.move
        self.team=ex_leaf.team
        self.parent=ex_leaf.parent
        self.children=[] # MUST BE EXPANDED AFTER CREATION
    
    def ucb_score(self):
        return self.score_sum/self.n_simu
    
    def score(self):
        if self.solved:
            return inf*self.exact_score  # type: ignore
        else:
            return self.ucb_score()

class TerminalNode():
    def __init__(self):
        self.exact_score=None  #1 for white win -1 for Black Win
        self.parent=None
        self.move=None
    
    def score(self):
        return inf*self.exact_score  # type: ignore
    
    def ucb_score(self):
        return self.exact_score

def Count_Leaves_In_Child(Node):
    if isinstance(Node,Leaf):
        return 'I am a leaf'
    else:
        counter=0
        for child in Node.children:
            if isinstance(child,Leaf):
                counter+=1
        return counter



class GenericMCTS(GenericAgent):

    def __init__(self,simu_time=1,verbose=True):
        self.simu_time=simu_time
        self.verbose=verbose
        self.tree_depth=0
        self.simulations_counter_total=0

    def new_game(self,starting_board,rules):
        self.rules=rules
        self.root=Root(starting_board.copy())
        self.expand(self.root)

    def select_child(self,node):
        ### 'TREE POLICY' -> Must be Overwritten
        return node.children[0]

    def eval(self,board):
        ### Evaluation -> Must be Overwritten
        return 0

    def init_score(self,node):
        # Note : if there was a winning TerminalNode 
        # this node would be 'solved' and this woud not be called
        # hence we can ignore the TerminalNode who are all lost

        children_scores=[]
        for child in node.children:
            if not(isinstance(child,TerminalNode)):
                children_scores.append(child.ucb_score())
        node.n_simu=len(children_scores)
        node.score_sum=sum([score for score in children_scores])

    def expand(self,node):

        # ------------------- Expand a Leaf (or the root) ------------------- #

        board=node.board

        if isinstance(node,Leaf):
            # ------------------- Swap Leaf with Node ------------------- #
            parent=node.parent
            new_node=Node(node)
            parent.children.remove(node)   # type: ignore
            parent.children.append(new_node)  # type: ignore
            node=new_node
        else:
            assert isinstance(node,Root)

        

        # ------------------- Create Children (leaves or Terminals) ------------------- #
        for valid_move in board.valid_moves: # type: ignore
            new_board=board.copy() # type: ignore
            self.rules.apply_move(new_board,valid_move) # type: ignore

            if new_board.current_color==None: #Terminal State
                child=TerminalNode()
                child.exact_score=2*self.rules.white_win(new_board)-1
                child.move=valid_move
            else:
                child=Leaf()
                child.move=valid_move
                if new_board.current_color=='White':
                    child.team=1 # type: ignore
                else:
                    child.team=-1 # type: ignore
                child.board=new_board
                child.temporary_score=self.eval(new_board)

            child.parent=node # type: ignore
            node.children.append(child) # type: ignore

        # ------------------- Init status 'solved ?' ------------------- #

        self.update_solve(node)
        
        # ------------------- Init the score of the expanded node ------------------- #
        if not(node.solved):
            self.init_score(node)

        # Return the node that has remplaced the leaf
        return node # type: ignore

    def update_solve(self,node):

        if node.solved:
            return

        lose=True
        win=False
        team=node.team
        for child in node.children:
            if isinstance(child,Leaf):
                lose=False  # Can't conlude that we lose if there is unexplored direction

            elif isinstance(child,Node):     
                if child.solved==False:
                    lose=False 
                else:
                    if child.exact_score==team:
                        win=True
                        lose=False
                        break
            elif isinstance(child,TerminalNode):
                if child.exact_score==team:
                        win=True
                        lose=False
                        break
        
        assert not(lose) or not(win)
        
        if lose:

            node.solved=True
            node.exact_score=-team
            node.n_simu=1
            node.score_sum=node.exact_score
            if not(isinstance(node,Root)):
                self.update_solve(node.parent)

        elif win:

            node.solved=True
            node.exact_score=team
            node.n_simu=1
            node.score_sum=node.exact_score
            if not(isinstance(node,Root)):
                self.update_solve(node.parent)

    def backprop(self,node):

        score=node.ucb_score()

        ancester=node.parent
        while not(isinstance(ancester,Root)):
            ancester.n_simu+=1 # type: ignore
            ancester.score_sum+=score # type: ignore
            ancester=ancester.parent # type: ignore
        ancester.n_simu+=1 # type: ignore
        ancester.score_sum+=score # type: ignore


    def simulation(self):

        current_node=self.root
        depth=0

        stopping_condition=False
        first=True
        while not(stopping_condition): 
            current_node=self.select_child(current_node)
            '''
            if first:
                print(current_node.move)
                first=False
            '''
            stopping_condition=isinstance(current_node,TerminalNode) or isinstance(current_node,Leaf)
            depth+=1

        self.tree_depth=max(self.tree_depth,depth)

        if isinstance(current_node,Leaf):
            current_node=self.expand(current_node)
        self.backprop(current_node)    # type: ignore


    def observe_move(self,new_move):
        new_board=self.root.board
        self.rules.apply_move(new_board,new_move)

        for child in self.root.children:
            if child.move==new_move:
                new_root=child
                break
        
        if isinstance(new_root,Leaf): # type: ignore
            #print('The Nex Root is a leaf :o')
            self.root=Root(new_board)
            self.expand(self.root)
            self.tree_depth=0

        elif isinstance(new_root,Node): # type: ignore
            self.root=Root(new_board)
            self.root.score_sum=new_root.score_sum 
            self.root.n_simu=new_root.n_simu 
            self.root.children=new_root.children 
            self.root.team=new_root.team 
            self.root.solved=new_root.solved
            self.root.exact_score=new_root.exact_score  # type: ignore
            self.tree_depth-=1
            for child in self.root.children:
                child.parent=self.root
        else:
            assert isinstance(new_root,TerminalNode) # type: ignore
            self.root=Root(new_board)

    def ask_move(self,rules,board,displayer):

        if self.verbose:
            print('')
        start_simu_time=time()
        N_simu=0
        while time()-start_simu_time<self.simu_time or N_simu==0:
            self.simulation()
            N_simu+=1

            if displayer!=None:
                displayer.do_nothing()

            if self.root.solved==True:
                if self.root.exact_score==self.root.team:  # type: ignore
                    if self.verbose:
                        print('Checkmate!')
                    break
        
        self.simulations_counter_total+=N_simu
        if self.verbose:
            if self.root.solved:
                print(f'Engame Solved, winner: {self.root.exact_score}')  # type: ignore
            else:
                print(f"Nombre simulation {N_simu}")
                print(f"Simulation/Seconde {int(N_simu/self.simu_time)}")
                print(f"Tree depth : {self.tree_depth}")
            print('Selecting my move :')
            k=0
            team=self.root.team
            for child in self.root.children:
                if isinstance(child,Leaf):
                    print(f'move : {child.move} = Leaf, won? : {(team*child.score()+1)/2}')
                elif isinstance(child,TerminalNode):
                    print(f'move : {child.move} = Terminal, won? : {(team*child.score()+1)/2}')  # type: ignore
                else:
                    if child.solved==True:
                        print(f'move : {child.move} = Solved Node, won? : {(team*child.exact_score+1)/2}')
                    else:
                        print(f'move : {child.move} = Node, explored {child.n_simu}x, winrate : {(team*child.score()+1)/2}')
                k+=1

        team=self.root.team
        if self.root.solved and self.root.exact_score!=self.root.team:
            greedy_score=[team*child.ucb_score()  for child in self.root.children]
        else:
            greedy_score=[team*child.score()  for child in self.root.children]
        choice=argmax(array(greedy_score))
        
        if self.verbose:
            print(f'Proba of winning, post tree search : {greedy_score[choice]/2+0.5}')
            
        return self.root.children[choice].move
            