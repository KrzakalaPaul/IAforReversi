from .linear_eval import LinearEvaluation
from agents.all_agents import EvalMCTS,FullRandomMCTS
from .data_set import generate_DSG,merge_DSG_list,merge_DSG
from arenas.simulator import fight
from copy import deepcopy


# V1 : Opponent Pool
def train_MCTS(eval:LinearEvaluation,N=8,N_outer=10,N_games=100,simu_time=3,save_name='unnamed_MCTS_training'):

    OpponentPool=[FullRandomMCTS(simu_time=simu_time,c=1,verbose=False)]
    Agent=FullRandomMCTS(simu_time=simu_time,c=1,verbose=False)
    
    for k_outer in range(N_outer):
        
        DSG_list=[]
        winrate_list=[]
        for opponent in OpponentPool:
            new_DSG,winrate=generate_DSG(Agent,opponent,N,N_games=N_games//len(OpponentPool),random_moves=2)
            winrate_list.append(winrate)
            DSG_list.append(new_DSG)
        
        DSG=merge_DSG_list(DSG_list)
        DSG.save(save_name+f'_iter{k_outer}')
            
        eval.fit(DSG)
        Agent=EvalMCTS(eval,simu_time=simu_time,c=1,n_simu_init=2, rollout_horizon=0, rollout_repeat=1 ,verbose=False)
        OpponentPool.append(deepcopy(Agent))  # type: ignore
        
        print('')
        print(f'Iteration {k_outer}')
        print('')
        print('params:')
        eval.print()
        print('')
        print('winrates:')
        print(winrate_list)
        print('')







