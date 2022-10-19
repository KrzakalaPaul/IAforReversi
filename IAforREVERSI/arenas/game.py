from reversi.board import Board
from reversi.rules import Rules
from display.displayer import Displayer

from agents.human_agent.human_class import HumanAgent

def game(Agent1,Agent2):

    players={"White" : Agent1, "Black" : Agent2}

    rules=Rules(N=8)
    board=rules.init_board()
    displayer=Displayer(board=board)

    Agent1.new_game(board,rules)
    Agent2.new_game(board,rules)

    while board.current_color in ['White','Black'] :
        
        current_player=players[board.current_color]

        if not(isinstance(current_player,HumanAgent)):
            displayer.computing=True

        move=current_player.ask_move(rules,board,displayer)
        
        displayer.computing=False

        assert rules.check_valid(board,move)

        rules.apply_move(board,move)
        Agent1.observe_move(move)
        Agent2.observe_move(board)

        displayer.update()

    



    
        
