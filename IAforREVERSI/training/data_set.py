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

    for game_counter in range(n_game):

        # Select Color 

        if game_counter%2==0:
            # Run Simulation with save
            label,save=simulator_with_save(Agent1,Agent2,N=N)
            
        else:
            # Run Simulation with save
            label,save=simulator_with_save(Agent2,Agent1,N=N)

        # Update Dataset
        for board_save in save:
            data_matrix.append(board_save.matrix)
            data_label.append(label)

        print(f"{int(100*game_counter/n_game)}%")

    np.savez_compressed(os.path.join(dataset_path, 'matrices'),data_matrix)
    np.save(os.path.join(dataset_path, 'labels'),np.array(data_label))

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
