from IAforREVERSI.reversi.board import Board
from IAforREVERSI.reversi.rules import Rules
from IAforREVERSI.display.displayer import Displayer

from IAforREVERSI.agents.human_agent.human_class import HumanAgent

def simulator(Agent1,Agent2):

    assert not(isinstance(Agent1,HumanAgent))
    assert not(isinstance(Agent2,HumanAgent))

    players={"White" : Agent1, "Black" : Agent2}

    rules=Rules(N=8)
    board=rules.init_board()
    displayer=None

    while board.current_color in ['White','Black'] :

        current_player=players[board.current_color]


        move=current_player.ask_move(rules,board,displayer)
        
        assert rules.check_valid(board,move)
        rules.apply_move(board,move)
