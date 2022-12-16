from agents.MCTS_agent.base_class import GenericMCTS,Root,TerminalNode,Leaf,Node
from agents.random_agent.random_class import RandomAgent
from arenas.simulator import simulator
from numpy import array,argmax,inf,log,sqrt
from random import choice

class FullRandomMCTS(GenericMCTS):

    def __init__(self,simu_time=1,c=sqrt(2),verbose=True):
        super().__init__(simu_time=simu_time,verbose=verbose)
        self.c=c
        self.rollout_agent=RandomAgent

    def eval(self,board_to_eval):

        white_score=simulator(self.rollout_agent(),self.rollout_agent(),N=self.rules.N,board=board_to_eval.copy())
        return 2*white_score-1


    def select_child(self,node):
        team=node.team
        N=node.n_simu
        ucb=[]


        # Try To build an UCB for non solved node:
        for child in node.children:

            if isinstance(child,Leaf) or isinstance(child,TerminalNode):
                n=1
                ucb.append(child.score()*team + self.c*sqrt(log(N)/n))
                
            else: 
                n=child.n_simu
                ucb.append(child.score()*team + self.c*sqrt(log(N)/n))

        return node.children[argmax(array(ucb))]
        





