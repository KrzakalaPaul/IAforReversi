from agents.all_agents import RandomAgent,FullRandomMCTS
import numpy as np
import matplotlib.pyplot as plt
from arenas.simulator import simulator,fight


def troncate(x):
    return min(x,100)
troncate=np.vectorize(troncate)

def time_plot(N=6,T=[0.01],repeat=200):

    time_complexity=0
    for t in T:
        time_complexity+=0.5*N**2*t*repeat
    print(f'Excpected computation time: {3*time_complexity/60}min')

    ci=100*np.sqrt((1/(8*repeat))*np.log(2/0.05))
    print(ci)
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
        y=np.array(winrate)
        ax.fill_between(T, (y-ci), troncate(y+ci), alpha=0.1)
        ax.plot(T, y,label=f'c={c}')

    ax.set_xlabel('Simulation Time t')
    ax.set_ylabel('Winrate against random agent')
    plt.legend()
    plt.show()

def c_plot(N=6,t=1e-3,C=np.array([0.1,1,10]),repeat=200):

    ci=100*np.sqrt((1/(8*repeat))*np.log(2/0.05))
    time_complexity=0.5*N**2*t*repeat*len(C)
    print(f'Excpected computation time: {3*time_complexity/60}min')

    fig,ax=plt.subplots()
    winrate=[]
    n_simus=[]
    for c in C:
        agent=FullRandomMCTS(simu_time=t,c=c,verbose=False,children_init='one') # type: ignore        
        wr=fight(agent,RandomAgent(),N=N,repeat=repeat,verbose=False)
        wr=100*wr/repeat
        winrate.append(wr)
        print(f'c:{c}, wr:{wr}%')

    y=np.array(winrate)
    ax.semilogx(C,y)
    ax.fill_between(C, (y-ci), troncate(y+ci), alpha=0.1)
    ax.plot(C, y)
    ax.set_xlabel('c')
    ax.set_ylabel('Winrate against random agent')
    plt.show()

def competition(agents_list,n_games,N):
    n_agents=len(agents_list)
    matrix=np.zeros((n_agents,n_agents))
    for i in range(n_agents):
        matrix[i,i]=n_games/2
        for j in range(i+1,n_agents):
            agenti=agents_list[i]
            agentj=agents_list[j]
            wini=fight(agenti,agentj,N=N,repeat=n_games,verbose=False)
            matrix[i,j]=wini
            matrix[j,i]=n_games-wini
            print(f'agent {i} wins {wini}/{n_games} vs agent {j}')
    print(matrix)

