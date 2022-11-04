from agents.MCTS_agent.full_random import FullRandomMCTS
from agents.MCTS_agent.base_class import GenericMCTS
from agents.random_agent.random_class import RandomAgent
from arenas.simulator import finite_horizon_simulator
from numpy import sqrt

class EvalMCTS(FullRandomMCTS):

    def __init__(self,eval_fct,simu_time=1,c=sqrt(2), rollout_horizon=0, rollout_repeat=1 ,verbose=True):
        super().__init__(c=c,simu_time=simu_time,verbose=verbose)
        self.c=c
        self.eval_fct=eval_fct
        self.rollout_agent=RandomAgent

        self.H=rollout_horizon
        self.k=rollout_repeat

    def eval(self,board_to_eval):
        
        avg_score=0

        for _ in range(self.k):

            horizon_board=finite_horizon_simulator(self.rollout_agent(),self.rollout_agent(),N=self.rules.N,board=board_to_eval.copy(),horizon=self.H)

            if horizon_board.current_color==None:
                white_value=self.rules.white_win(horizon_board)
            else:
                white_value=self.eval_fct(horizon_board)

            if board_to_eval.current_color=='White':
                avg_score+= white_value

            else :
                avg_score+= 1-white_value

        return avg_score/self.k

    def ask_move(self,rules,board,displayer):
        if self.verbose:
            eval_white_win=self.eval_fct(board)
            if board.current_color=='White':
                print(f'Proba of winning, fast eval : {eval_white_win}')
            else:
                print(f'Proba of winning, fast eval : {1-eval_white_win}')
        return super().ask_move(rules,board,displayer)