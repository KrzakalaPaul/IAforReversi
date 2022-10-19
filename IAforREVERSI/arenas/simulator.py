from reversi.board import Board
from reversi.rules import Rules
from display.displayer import Displayer

from agents.human_agent.human_class import HumanAgent

def simulator(WhiteAgent,BlackAgent,N=8,board=None):

    players={"White" : WhiteAgent, "Black" : BlackAgent}

    assert not(isinstance(WhiteAgent,HumanAgent))
    assert not(isinstance(BlackAgent,HumanAgent))

    rules=Rules(N=N)
    if board==None:
        board=rules.init_board()

    WhiteAgent.new_game(board,rules)
    BlackAgent.new_game(board,rules)

    while board.current_color in ['White','Black'] :
        
        current_player=players[board.current_color]
        move=current_player.ask_move(rules,board,None)
        assert rules.check_valid(board,move)
        rules.apply_move(board,move)
        WhiteAgent.observe_move(move)
        BlackAgent.observe_move(move)


    return rules.white_win(board)

from numpy.random import randint

def fight(Agent1,Agent2,N=8,repeat=100,refresh_rate=10):

    print('Fight Starting :')
    
    win1=0
    for k in range(repeat):
        randomize=randint(0,2)
        if randomize==0:
            results=simulator(Agent1,Agent2,N=N)
            win1+=results
        else:
            results=simulator(Agent2,Agent1,N=N)
            win1+=1-results

        if k%refresh_rate==0:
            print('')
            print(f'Fight {int(100*(k+1)/repeat)}% complete')
            print(f'Agent1 winrate so far : {int(100*win1/(k+1))}%')

    return win1