import os as os 

def TrainLinearEvaluation(eval_class,H=1,k=1,t=0.1,n_eval=100,n_update=100,save=None):
    # eval_class = The class of linear evaluation to train 
    # H = Rollout horizon
    # k = Number of rollout/eval for evaluation
    # t = time budget for 1 move
    # n_eval = Number of game between update of the parameter
    # n_update = number of parameter update

    print(os.getcwd())

    if save!=None:
        # TO DO : 
        # Load Pool of opponents
        pass

    else:
        # TO DO : setup save folder, init parameter, save init param in the folder
        Opponent_Pool=[]
        # Init Pool of opponents with fullrandom MCTS
        pass


    for update_counter in range(n_update):

        # Setup agent to evaluate

        # Initialize empty dateset features/winner

        for simulation_counter in range(n_eval):

            # Select Opponent
            # Select Color 
            # Run Simulation with save
            # Save -> Dataset (matrix -> features)
                
        # update param
        # save old params in directory 
        # update pool of opponents

                pass