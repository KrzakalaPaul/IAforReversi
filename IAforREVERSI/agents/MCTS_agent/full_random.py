from agents.MCTS_agent.base_class import GenericMCTS,Root,TerminalNode,Leaf,Node
from agents.random_agent.random_class import RandomAgent
from arenas.simulator import simulator
from numpy import array,argmax,inf,log,sqrt
from random import choice

class FullRandomMCTS(GenericMCTS):

    def __init__(self,simu_time=1,c=sqrt(2),verbose=True,children_init='one',rollout_agent=RandomAgent):
        super().__init__(simu_time=simu_time,verbose=verbose)
        self.c=c
        self.children_init=children_init
        self.rollout_agent=rollout_agent

    def init_score(self,node):
        children_scores=[]
        for child in node.children:
            if not(isinstance(child,TerminalNode)):
                if child.n_simu>0:
                    children_scores.append(child.score_bounded())
        node.n_simu=len(children_scores)
        node.score_sum=sum([score for score in children_scores])



    def init_children_score(self,node):
        if self.children_init=='all':
            for child in node.children:
                if isinstance(child,Leaf):
                    child.n_simu=1
                    child.temporary_score=self.eval(child.board)
        else:
            child_list=[]
            for child in node.children:
                if isinstance(child,Leaf):
                    child_list.append(child)
            child=choice(child_list)
            child.n_simu=1
            child.temporary_score=self.eval(child.board)


    def eval(self,board_to_eval):

        white_score=simulator(self.rollout_agent(),self.rollout_agent(),N=self.rules.N,board=board_to_eval.copy())
        return 2*white_score-1


    def select_child(self,node):
        team=node.team
        N=node.n_simu
        ucb=[]


        # Try To build an UCB for non solved node:
        for child in node.children:

            if isinstance(child,TerminalNode):
                ucb.append(child.score()*team)
            elif isinstance(child,Leaf):
                if child.n_simu==0:
                    ucb.append(+inf)
                else:
                    n=child.n_simu
                    ucb.append(child.score()*team + self.c*sqrt(log(N)/n))
            else: 
                n=child.n_simu
                ucb.append(child.score()*team + self.c*sqrt(log(N)/n))

        return node.children[argmax(array(ucb))]
        





