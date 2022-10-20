from agents.all_agents import RandomAgent,FullRandomMCTS
import numpy as np
import matplotlib.pyplot as plt
from arenas.simulator import simulator,fight

def Plot():
    plt.figure()
    for N in [4]:
        T=np.linspace(0.01,0.02,2)*N/4  # type: ignore
        winrate=[]
        for t in T:
            wr=fight(FullRandomMCTS(simu_time=t,verbose=True),RandomAgent(),N=N,repeat=100,verbose=False)
            winrate.append(wr)
        plt.plot(T,np.array(winrate))
    plt.show()

