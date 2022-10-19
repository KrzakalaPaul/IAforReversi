from agents.MCTS_agent.base_class import GenericMCTS,Node,TerminalNode
from agents.random_agent.random_class import RandomAgent
from arenas.simulator import simulator
from numpy import array,argmax,inf,log,sqrt

class FullRandomMCTS(GenericMCTS):

    def __init__(self,N_simulation=100,N_rollout=10,c=sqrt(2)):
        self.N_simulation=N_simulation 
        self.N_rollout=N_rollout
        self.c=c

    def eval(self,board_to_eval):
        
        avg_white_score=0
        for _ in range(self.N_rollout):
            avg_white_score+=simulator(RandomAgent(),RandomAgent(),N=self.rules.N,board=board_to_eval.copy())

        avg_white_score=avg_white_score/self.N_rollout

        if board_to_eval.current_color=='White':
            return self.N_rollout,avg_white_score

        else :
            return self.N_rollout,1-avg_white_score
        

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
                white_score=child.white_score

                if team=='White':
                    ucb.append(white_score + self.c*log(N)/n)
                else:
                    ucb.append(1-white_score + self.c*sqrt(log(N)/n))
            
            
        return argmax(array(ucb))

        









