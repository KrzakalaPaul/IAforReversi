from reversi.board import Board
from reversi.rules import Rules
from display.displayer import Displayer
from reversi.heuristics import potential_mobility
from agents.human_agent.human_class import HumanAgent

def game(WhiteAgent,BlackAgent,N=8):

    players={"White" : WhiteAgent, "Black" : BlackAgent}

    rules=Rules(N=N)
    board=rules.init_board()
    displayer=Displayer(board=board)

    WhiteAgent.new_game(board,rules)
    BlackAgent.new_game(board,rules)

    while board.current_color in ['White','Black'] :
        
        current_player=players[board.current_color]

        if not(isinstance(current_player,HumanAgent)):
            displayer.computing=True

        move=current_player.ask_move(rules,board,displayer)
        
        displayer.computing=False

        assert rules.check_valid(board,move)

        rules.apply_move(board,move)
        WhiteAgent.observe_move(move)
        BlackAgent.observe_move(move)
        displayer.update()

    displayer.wait()

    



    
        
