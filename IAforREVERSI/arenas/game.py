from IAforREVERSI.reversi.board import Board
from IAforREVERSI.reversi.rules import Rules
from IAforREVERSI.display.displayer import Displayer

from IAforREVERSI.agents.human_agent.human_class import HumanAgent

def game(Agent1,Agent2):

    players={"White" : Agent1, "Black" : Agent2}

    rules=Rules(N=8)
    board=rules.init_board()
    displayer=Displayer(board=board)

    while board.current_color in ['White','Black'] :

        current_player=players[board.current_color]

        if not(isinstance(current_player,HumanAgent)):
            displayer.computing=True

        move=current_player.ask_move(rules,board,displayer)
        
        displayer.computing=False

        assert rules.check_valid(board,move)
        rules.apply_move(board,move)
        displayer.update()

    



    
        
