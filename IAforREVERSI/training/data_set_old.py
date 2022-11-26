from reversi.board import Board
import os 
import numpy as np
from arenas.simulator import simulator_with_save

def CreateDataSet(name,Agent1,Agent2,n_game=100,N=8):
    save_path = os.path.join(os.getcwd(), 'IAforREVERSI\\saves')
    dataset_path=os.path.join(save_path, 'dataset\\'+name)

    try: 
        os.makedirs(dataset_path)
    except OSError:
        pass

    data_matrix=[]
    data_label=[]

    Win_rate_1=0
    Nb_games=0

    for game_counter in range(n_game):

        # Select Color 

        if game_counter%2==0:
            # Run Simulation with save
            label,save=simulator_with_save(Agent1,Agent2,N=N)
            Win_rate_1+=label
            Nb_games+=1
            
        else:
            # Run Simulation with save
            label,save=simulator_with_save(Agent2,Agent1,N=N)
            Win_rate_1+=1-label
            Nb_games+=1

        # Update Dataset
        for board_save in save:
            data_matrix.append(board_save.matrix)
            data_label.append(label)

        print(f"{int(100*game_counter/n_game)}%")
        print(f' Win rate agent1 : {int(100*Win_rate_1/Nb_games)}%')

    np.savez_compressed(os.path.join(dataset_path, 'matrices'),data_matrix)
    np.save(os.path.join(dataset_path, 'labels'),np.array(data_label))

    return Win_rate_1/Nb_games

def UnionDataSet(names,union_name):

    all_data_matrix=[]
    all_data_label=[]

    for name in names :
        data_board,data_label=LoadDataSet(name)

        for board,label in zip(data_board,data_label):
            all_data_matrix.append(board.matrix)
            all_data_label.append(label)
    
    save_path = os.path.join(os.getcwd(), 'IAforREVERSI\\saves')
    dataset_path=os.path.join(save_path, 'dataset\\'+union_name)

    try: 
        os.makedirs(dataset_path)
    except OSError:
        pass

    np.savez_compressed(os.path.join(dataset_path, 'matrices'),all_data_matrix)
    np.save(os.path.join(dataset_path, 'labels'),np.array(all_data_label))
        

def LoadDataSet(name):
    
    save_path = os.path.join(os.getcwd(), 'IAforREVERSI\\saves')
    dataset_path=os.path.join(save_path, 'dataset\\'+name)

    data_label=np.load(os.path.join(dataset_path, 'labels.npy'))
    n=len(data_label)
    loaded_matrices =np.load(os.path.join(dataset_path, 'matrices.npz'))
    data_board=[]
    matrices=loaded_matrices[f'arr_0']

    for i in range(n):
        board=Board(matrix=matrices[i],current_color='not saved')
        data_board.append(board)

    return data_board,data_label
