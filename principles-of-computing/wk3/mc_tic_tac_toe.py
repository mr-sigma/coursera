"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 0.8 # Score for squares played by the current player
SCORE_OTHER = 1.5   # Score for squares played by the other player

EMPTY = 1
PLAYERX = 2
PLAYERO = 3 
DRAW = 4

STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}


    
# Add your functions here.

def score_grid_init(board):
    """
    Initializes a score matrix with all zeroes
    returns the zeroed board.
    """
    dim = board.get_dim()
    score_grid = [[0 for dummycol in range(dim)] 
                           for dummyrow in range(dim)]
    return score_grid
    

# May want to use the clone method to provide the 
# current board to all these functions.
def mc_trial(board, player):
    """
    Takes current board and the next player to move.
    Plays a game making random moves function modifies
    the board input and does not return anything.
    """
    
    empties = board.get_empty_squares()
    while len(empties) > 0:
        random.shuffle(empties)
        row, column = empties.pop()
        board.move(row, column, player)
        player = provided.switch_player(player)
        if board.check_win() != None:
            break

def mc_update_scores(scores, board, player):
    """
    Takes grid of scores as a list of lists with
    same dimension as Tic-Tac-Toe board, a board
    from a completed game, and which palyer the 
    machine is. Scores completed board and updates
    the scores. Does not return anything.
    """
    
    # check who won
    outcome = board.check_win()
    other_player = provided.switch_player(player)
    if outcome == DRAW:
        pass
    elif outcome == player:
        # machine won -- tally appropriately
        for row in range(len(scores)):
            for col in range(len(scores[0])):
                if board.square(row, col) == player:
                    #favor entries that lead to a win
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == other_player:
                    # discourage machine from taking
                    # a spot which caused the opponent
                    # to lose
                    scores[row][col] -= SCORE_OTHER
                else:
                    # ignore all other spaces
                    continue
    elif outcome == other_player:
        # other player won -- tally appropriately
        for row in range(len(scores)):
            for col in range(len(scores[0])):
                if board.square(row, col) == player:
                    # discourage entries that lead 
                    # to a loss
                    scores[row][col] -= SCORE_CURRENT
                elif board.square(row, col) == other_player:
                    # encourage machine to take
                    # a spot which caused the opponent
                    # to win
                    scores[row][col] += SCORE_OTHER
                else:
                    # ignore all other spaces
                    continue                
    else:
        print "Something unexpected happened in mc_update_scores"

def get_best_move(board, scores):
    """
    Takes current board and scores. Finds the empty
    squares with the maximum score and randomly
    returns one of them as (row, column) tuple.
    If no moves left, will return None
    """
    
    # use the Tic-Tac-Toe get_empty_squares
    # to get a list of tuples containing empty
    # squares
    empties = board.get_empty_squares()
    empties_scores = []
    # if there are no moves remaning
    # returns None
    if len(empties) < 1:
        return None
    # create list of scores corresponding to empty squares
    empties_scores = [scores[row][col] for row,col in empties]
    # find the max score (best move)
    best_move = max(empties_scores)
    # create a list of tuples for the squares
    # with the maximum score and return a
    # random entry from it
    best_moves = [empties[index] for index, entry \
                  in enumerate(empties_scores) \
                  if entry == best_move]
    return random.choice(best_moves)

def mc_move(board, player, trials):
    """
    Takes current board, which player the machine
    is, and the number of trials to run.
    Runs a Monte Carlo and returns a move for the
    machine player as (row, column) tuple.
    """
    
    # initialize score matrix valid
    # for all trials
    scores = score_grid_init(board)
    
    # create a loop for the number of trials
    for dummy_i in range(trials):
        # make a copy of the board to operate on
        board_copy = board.clone()
        # run the trial
        mc_trial(board_copy, player)
        mc_update_scores(scores, board_copy, player)
    
    # will end up returning get_best_move()
    return get_best_move(board, scores)

#---------------------------------------
# Tests
#---------------------------------------

# mc_trial
#test_board = provided.TTTBoard(3)
#test_player = PLAYERX
#
#mc_trial(test_board, test_player)
#print test_board

# scoring trial
#score_board = score_grid_init(test_board)
#print score_board
#
#mc_update_scores(score_board, test_board, test_player)
#print score_board
#
#print get_best_move(test_board, score_board)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
