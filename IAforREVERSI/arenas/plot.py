from agents.all_agents import RandomAgent,FullRandomMCTS
import numpy as np
import matplotlib.pyplot as plt
from arenas.simulator import simulator,fight

def Plot():
    plt.figure()
    for N in [6]:
        T=np.linspace(0.2,0.2,10)*N/4  # type: ignore
        winrate=[]
        for t in T:
            wr=fight(FullRandomMCTS(simu_time=t,verbose=True),RandomAgent(),N=N,repeat=100,verbose=True)
            winrate.append(wr)
        plt.plot(T,np.array(winrate))
    plt.show()

