from agents.all_agents import FullRandomMCTS,EvalMCTS
import os 
from random import choice
import numpy as np
from numpy.random import randint
from arenas.simulator import simulator_with_save
from tqdm import tqdm
from copy import deepcopy
from .data_set import LoadDataSet


def TrainLinearEvaluation(eval_fct,H=1,k=1,t=0.1,n_eval=100,n_update=100,save=None,precomputed_data_set=None):
    # eval_class = The class of linear evaluation to train 
    # H = Rollout horizon
    # k = Number of rollout/eval for evaluation
    # t = time budget for 1 move
    # n_eval = Number of game between update of the parameter
    # n_update = number of parameter update

    N=eval_fct.N
    dim=eval_fct.dim

    save_path = os.path.join(os.getcwd(), 'IAforREVERSI\\saves')
    run_path =''
    if save!=None:
        # Load Pool of opponents agent
        run_path =save

        Opponent_Pool=[FullRandomMCTS(simu_time=t,verbose=False)]  # type: ignore
        
        update_counter=0
        np_path=os.path.join(run_path,f"coef_{update_counter}")
        while os.path.isfile(np_path):

            eval_fct.load(np_path)
            Opponent_Pool.append(EvalMCTS(deepcopy(eval_fct),simu_time=t, rollout_horizon=H, rollout_repeat=k,verbose=False ))  # type: ignore

            update_counter+=1
            np_path=os.path.join(run_path,f"coef_{update_counter}")

        Agent=EvalMCTS(deepcopy(eval_fct),simu_time=t, rollout_horizon=H, rollout_repeat=k,verbose=False)  # type: ignore

    else:
        # CREATE NEW FOLDER 
        i=0
        folder_created=False
        while not(folder_created):
            run_path=os.path.join(save_path, f"{eval_fct.__class__.__name__}_run_{i}")
            try: 
                os.makedirs(run_path)

                readme_path=os.path.join(run_path,"readme.txt")
                with open(readme_path, 'w') as f:
                    f.write(f'{(eval_fct.__class__.__name__,N,H,k,t,n_eval,n_update)}')

                folder_created=True
            except OSError:
                i+=1

        Opponent_Pool=[FullRandomMCTS(simu_time=t,verbose=False)]  # type: ignore
        Agent=FullRandomMCTS(simu_time=t,verbose=False) # type: ignore

        if precomputed_data_set!=None:

            data_board,data_label=LoadDataSet(precomputed_data_set)
            data_features=[eval_fct.features(board) for board in data_board]
            data_features=np.concatenate(data_features)

            

            eval_fct.model.fit(X=data_features,y=data_label)

            print(eval_fct.model.coef_)
            # save old params in directory 
            np_path=os.path.join(run_path,f"coef_{-1}")
            np.save(np_path,eval_fct.model.coef_)

            # update pool of opponents
            Opponent_Pool.append(EvalMCTS(deepcopy(eval_fct),simu_time=t, rollout_horizon=H, rollout_repeat=k,verbose=False ))  # type: ignore
            Agent=EvalMCTS(deepcopy(eval_fct),simu_time=t, rollout_horizon=H, rollout_repeat=k,verbose=False)  # type: ignore

            
    for update_counter in range(n_update):

        # Setup agent to evaluate
        pool_size=len(Opponent_Pool)
        Win_rate=np.zeros(pool_size)
        Nb_games=np.zeros(pool_size)

        # Initialize empty dateset features/winner
        data_features=[]
        data_label=[]

        print("New simulation set")
        #for simulation_counter in tqdm(range(n_eval)):
        for simulation_counter in range(n_eval):
            # Select Opponent
            Opponent_id=choice(np.arange(pool_size))
            Opponent=Opponent_Pool[Opponent_id]

            # Select Color 

            if simulation_counter%2==0:
                # Run Simulation with save
                label,save=simulator_with_save(Agent,Opponent,N=N)
                
                # Save Winner for stats
                Win_rate[Opponent_id]+=label
                Nb_games[Opponent_id]+=1

                
            else:
                # Run Simulation with save
                label,save=simulator_with_save(Opponent,Agent,N=N)

                # Save Winner for stats
                Win_rate[Opponent_id]+=1-label
                Nb_games[Opponent_id]+=1

            # Update Dataset
            for board_save in save:
                data_features.append(eval_fct.features(board_save))
                data_label.append(label)

            print(f"{int(100*simulation_counter/n_eval)}%")

        data_label=np.array(data_label)
        data_features=np.concatenate(data_features)

        # update param
        print(data_label)
        print(data_features)
        eval_fct.model.fit(X=data_features,y=data_label)
        print(eval_fct.model.coef_)
        # save old params in directory 
        np_path=os.path.join(run_path,f"coef_{update_counter}")
        np.save(np_path,eval_fct.model.coef_)

        # update pool of opponents
        Opponent_Pool.append(EvalMCTS(deepcopy(eval_fct),simu_time=t, rollout_horizon=H, rollout_repeat=k,verbose=False ))  # type: ignore
        Agent=EvalMCTS(deepcopy(eval_fct),simu_time=t, rollout_horizon=H, rollout_repeat=k,verbose=False)  # type: ignore


        # Display stats:
        print("")
        print(f"Agent : {update_counter}")
        Win_rate=Win_rate/(Nb_games+1e-6)
        print(f"Win rate against previous agents : {Win_rate}")

    return Opponent_Pool 