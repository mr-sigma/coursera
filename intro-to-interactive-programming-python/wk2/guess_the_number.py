# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random

global game_range
game_range = "100"


# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    if game_range == "100":
        range100()
    elif game_range == "1000":
        range1000()
    else:
        print "Error in game_range"
    
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secret_number
    global remaining_guesses
    global game_range
    secret_number = random.randrange(0,100)
    remaining_guesses = 7
    game_range = "100"
    print ""
    print "New game"
    print "I'm thinking of a number between 0 and 100..."
    print "Remaining guesses:", remaining_guesses

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number
    global remaining_guesses
    global game_range
    secret_number = random.randrange(0,1000)
    remaining_guesses = 10
    game_range = "1000"
    print ""
    print "New game"
    print "I'm thinking of a number between 0 and 1000..."
    print "Remaining guesses:", remaining_guesses
    
def input_guess(guess):
    global secret_number
    global remaining_guesses
    guess_num = int(guess)
    print "Guess was", guess 
    remaining_guesses -= 1
    print "Remaining guesses:", remaining_guesses
    if guess_num == secret_number:
        print "Correct, you win!"
        print ""
        new_game()
    elif remaining_guesses <= 0:
        print "Out of guesses, you lose!"
        print ""
        new_game()
    elif guess_num < secret_number:
        print "Higher"
    elif guess_num > secret_number:
        print "Lower"
        

    
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0,100)", range100, 100)
frame.add_button("Range is [0,1000)", range1000, 100)
frame.add_input("Guess", input_guess, 100)


# call new_game 
new_game()
frame.start()
# always remember to check your completed program against the grading rubric

