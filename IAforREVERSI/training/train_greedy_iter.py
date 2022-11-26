

from .linear_eval import LinearEvaluation
from agents.all_agents import GreedyAgent,RandomAgent
from .data_set import generate_DSG
from arenas.simulator import fight

def train_greedy(eval:LinearEvaluation,N=8,N_outer=10,N_games=100,eps=0.01,verbose=True):

    for k_outer in range(N_outer):

        if k_outer==0:
            Agent1=RandomAgent()
            Agent2=RandomAgent()
        else:
            Agent1=GreedyAgent(eval,eps=eps)
            Agent2=GreedyAgent(eval,eps=eps)

        DSG=generate_DSG(Agent1,Agent2,N,N_games)
        
        eval.fit(DSG)
        print(f'Iteration {k_outer}, winrate against random agent: {fight(Agent1,Agent2,N=N,repeat=100,verbose=False)}')