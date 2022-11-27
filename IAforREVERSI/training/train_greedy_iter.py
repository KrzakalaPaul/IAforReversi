

from .linear_eval import LinearEvaluation
from agents.all_agents import GreedyAgent,RandomAgent
from .data_set import generate_DSG,merge_DSG_list,merge_DSG
from arenas.simulator import fight
from copy import deepcopy


# V1 : Opponent Pool
def train_greedy(eval:LinearEvaluation,N=8,N_outer=10,N_games=100,eps=0.01,verbose=True):

    OpponentPool=[RandomAgent()]
    Agent=RandomAgent()

    for k_outer in range(N_outer):
        
        DSG_list=[]
        for opponent in OpponentPool:
            DSG_list.append(generate_DSG(Agent,opponent,N,N_games=N_games//len(OpponentPool)))
        
        DSG=merge_DSG_list(DSG_list)
            
        eval.fit(DSG)
        Agent=GreedyAgent(eval,eps=eps) # type: ignore
        OpponentPool.append(deepcopy(Agent))  # type: ignore
        
        if verbose:
            eval.print()
            print(f'Iteration {k_outer}, winrate against random agent: {fight(GreedyAgent(eval,eps=None),RandomAgent(),N=N,repeat=100,verbose=False)}')
            
'''
# V2 : Stack DSG
def train_greedy(eval:LinearEvaluation,N=8,N_outer=10,N_games=100,eps=0.01,verbose=True):

    Opponent=RandomAgent()
    Agent=RandomAgent()
    for k_outer in range(N_outer):
        
        new_DSG=generate_DSG(Agent,Opponent,N,N_games=N_games)

        if k_outer==0:
            DSG=new_DSG
        else:
            DSG=merge_DSG(DSG,new_DSG) # type: ignore
            
        eval.fit(DSG)
        Agent=GreedyAgent(eval,eps=eps) # type: ignore
        Opponent=GreedyAgent(eval,eps=eps)
        
        if verbose:
            eval.print()
            print(f'Iteration {k_outer}, winrate against random agent: {fight(GreedyAgent(eval,eps=None),RandomAgent(),N=N,repeat=100,verbose=False)}')
'''