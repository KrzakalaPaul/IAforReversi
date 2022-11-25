from agents.all_agents import RandomAgent,FullRandomMCTS
import numpy as np
import matplotlib.pyplot as plt
from arenas.simulator import simulator,fight

def time_plot(N=6,T=[0.01]):

    winrate=[]
    n_simus=[]
    for t in T:
        agent=FullRandomMCTS(simu_time=t,c=50,verbose=False)
        wr=fight(agent,RandomAgent(),N=N,repeat=100,verbose=True)
        winrate.append(wr)
        n_simus.append(agent.simulations_counter_total)
    winrate.append(100)
    T.append(1)
    T=np.array(T)
    print(T)
    print(winrate)
    fig,ax=plt.subplots()
    ax.semilogx(T,np.array(winrate))
    ax.set_xlabel('Simulation Time t')
    ax.set_ylabel('Winrate against random agent')

    plt.show()



