"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    current_best_score = -1
    current_best_move = (-1, -1)
    empty_squares = board.get_empty_squares()
    
    # if there are no squares left, score board and 
    # return invalid move
    if len(empty_squares) == 0:
        return SCORES[board.check_win()], (-1, -1)

    # else go through all the possible moves
    for (row, col) in empty_squares:
        copied_board = board.clone()
        copied_board.move(row, col, player)
        score,dummy_move = mm_move(copied_board, provided.switch_player(player))    # for grader add provided.
        # cut the loop if the best move is found for
        # the current player
        if score * SCORES[player] == 1:
            return score, (row, col)
        # update the score if the move is better
        elif score * SCORES[player] > current_best_score:
            current_best_score = score
            current_best_move = (row, col)
        # take the last move if both are terrible
        elif current_best_score == -1:
            current_best_move = (row,col)
            
    # if all moves are exhausted without a win condition
    # return the best move
    return current_best_score * SCORES[player], current_best_move

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
