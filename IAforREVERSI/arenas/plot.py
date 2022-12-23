from agents.all_agents import RandomAgent,FullRandomMCTS
import numpy as np
import matplotlib.pyplot as plt
from arenas.simulator import simulator,fight

def time_plot(N=6,T=[0.01],repeat=200):

    fig,ax=plt.subplots()

    for c in [0.1,1,10]:

        winrate=[]
        n_simus=[]
        for t in T:
            agent=FullRandomMCTS(simu_time=t,c=c,verbose=False,children_init='one')
            wr=fight(agent,RandomAgent(),N=N,repeat=repeat,verbose=False)
            wr=100*wr/repeat
            winrate.append(wr)
            n_simus.append(agent.simulations_counter_total)
            print(f't:{t}, wr:{wr}%')
        T=np.array(T)
        ax.semilogx(T,np.array(winrate),label=f'c={c}')

    ax.set_xlabel('Simulation Time t')
    ax.set_ylabel('Winrate against random agent')
    plt.show()

def c_plot(N=6,C=[0.1,1,10],repeat=200):

    fig,ax=plt.subplots()
    t=1e-4
    winrate=[]
    n_simus=[]
    for c in C:
        agent=FullRandomMCTS(simu_time=t,c=c,verbose=False,children_init='one') # type: ignore        
        wr=fight(agent,RandomAgent(),N=N,repeat=repeat,verbose=False)
        wr=100*wr/repeat
        winrate.append(wr)
        #n_simus.append(agent.simulations_counter_total)
        print(f'c:{c}, wr:{wr}%')

    C=np.array(C)
    ax.semilogx(C,np.array(winrate))
    ax.set_xlabel('c')
    ax.set_ylabel('Winrate against random agent')
    plt.show()


