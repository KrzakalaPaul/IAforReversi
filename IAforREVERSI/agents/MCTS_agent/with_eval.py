from agents.MCTS_agent.full_random import FullRandomMCTS
from agents.MCTS_agent.base_class import GenericMCTS
from agents.random_agent.random_class import RandomAgent
from arenas.simulator import finite_horizon_simulator
from .base_class import TerminalNode
from numpy import sqrt

class EvalMCTS(FullRandomMCTS):

    def __init__(self,eval_fct,simu_time=1,c=sqrt(2),n_simu_init=2, rollout_horizon=0, rollout_repeat=1 ,verbose=True):
        super().__init__(c=c,simu_time=simu_time,verbose=verbose)
        self.c=c
        self.eval_fct=eval_fct
        self.rollout_agent=RandomAgent
        self.n_simu_init=n_simu_init

        self.H=rollout_horizon
        self.k=rollout_repeat

    def eval(self,board_to_eval):
        
        avg_score=0

        for _ in range(self.k):

            horizon_board=finite_horizon_simulator(self.rollout_agent(),self.rollout_agent(),N=self.rules.N,board=board_to_eval.copy(),horizon=self.H)

            if horizon_board.current_color==None:
                score=2*self.rules.white_win(horizon_board)-1
            else:
                score=2*self.eval_fct(horizon_board)-1
            avg_score+=avg_score

        return avg_score/self.k

    def ask_move(self,rules,board,displayer):
        if self.verbose:
            eval_white_win=self.eval_fct(board)
            if board.current_color=='White':
                print(f'Proba of winning, fast eval : {eval_white_win}')
            else:
                print(f'Proba of winning, fast eval : {1-eval_white_win}')
        return super().ask_move(rules,board,displayer)

    def init_score(self,node):
        # Note : if there was a winning TerminalNode 
        # this node would be 'solved' and this woud not be called
        # hence we can ignore the TerminalNode who are all lost

        children_scores=[]
        for child in node.children:
            if not(isinstance(child,TerminalNode)):
                children_scores.append(child.ucb_score())
        node.n_simu=self.n_simu_init
        team=node.team # type: ignore
        minimax_score=max([team*score for score in children_scores])
        node.score_sum=team*self.n_simu_init*minimax_score # type: ignore
