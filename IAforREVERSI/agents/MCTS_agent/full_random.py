from agents.MCTS_agent.base_class import GenericMCTS,Node,TerminalNode
from agents.random_agent.random_class import RandomAgent
from arenas.simulator import simulator
from numpy import array,argmax,inf,log,sqrt
from random import choice

class FullRandomMCTS(GenericMCTS):

    def __init__(self,simu_time=1,c=sqrt(2),verbose=True):
        super().__init__(simu_time=simu_time,verbose=verbose)
        self.c=c
        self.rollout_agent=RandomAgent()

    def eval(self,board_to_eval):

        white_score=simulator(self.rollout_agent,self.rollout_agent,N=self.rules.N,board=board_to_eval.copy())

        if board_to_eval.current_color=='White':
            return white_score

        else :
            return 1-white_score

    def eval_children(self,node,board_simulation):
        # Check if a move lead to a postive terminal state
        # If not rollout eval of one children at random

        non_terminal_child=[]
        for k,child in enumerate(node.children):
            if isinstance(child,TerminalNode):
                if node.team==child.winner:
                    return [k]
            else:
                non_terminal_child.append(k)
                
        if non_terminal_child==[]:
            return [0]

        k=choice(non_terminal_child)
        board_to_eval=board_simulation.copy()
        self.rules.apply_move(board_to_eval,node.moves[k])
        value=self.eval(board_to_eval)
        node.children[k].n_simu=1
        node.children[k].reward_sum=value
        return [k]

    def select_child(self,node):
        team=node.team
        N=node.n_simu
        ucb=[]
        for child in node.children:


            if isinstance(child,TerminalNode):
                if team=='White':
                    ucb.append((child.white_win-0.5)*inf)
                else:
                    ucb.append(-(child.white_win-0.5)*inf)

            else:
                n=child.n_simu

                if n==0:
                    ucb.append(+inf)
                else:
                    white_score=child.white_score()
                    if team=='White':
                        ucb.append(white_score + self.c*sqrt(log(N)/n))
                    else:
                        ucb.append(1-white_score + self.c*sqrt(log(N)/n))
            
        return argmax(array(ucb))

        









