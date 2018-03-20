# template for "Stopwatch: The Game"
import simplegui
import math

# define global variables

ds = 0 # Using deciseconds
num_stops = 0 # number of times the stopwatch is stopped
player_correct = 0 # number of times the player stops the watch on a whole number
clock_running = False # Boolean for whether the clock is running


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    t_copy = t
    hour = 0
    minute = 0
    second = 0
    deci = 0
    
    # Break off deciseconds
    deci = t_copy % 10    
    t_copy = int(math.floor(t_copy/10))
    
    # Break off seconds
    second = t_copy % 60    
    t_copy = int(math.floor(t_copy/60))
    
    # Break off minutes
    minute = t_copy % 60
    
    if minute < 10: # Add any leading zeros needed to minutes
        min_str = "0" + str(minute)
    else:
        min_str = str(minute)     
        
    if second < 10: # Add any leading zeros needed to seconds
        sec_str = "0" + str(second)
    else:
        sec_str = str(second)
        
    deci_str = str(deci)
    
    # return the properly formatted string
    return min_str + ":" + sec_str + "." + deci_str
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global num_stops, player_correct, clock_running
    clock_running = True # Set Boolean
    timer.start() # Start the timer
    
def stop():
    global ds, num_stops, player_correct, clock_running
    timer.stop() # Stop the timer
    
    # Check that the clock was running and change score
    if clock_running == True:
        clock_running = False
        num_stops += 1
        if ds % 10 == 0:
            player_correct += 1
    # Else nothing happens
    
def reset():
    """Reset the global variables to zero out stopwatch
       and the player guesses"""
    global ds, num_stops, player_correct
    timer.stop()
    ds = num_stops = player_correct = 0
    
    

# define event handler for timer with 0.1 sec interval
def tick():
    global ds
    ds += 1
    
        

# define draw handler
def draw_handler(canvas):
    global ds, num_stops, player_correct
    canvas.draw_text(format(ds),[220,250],34, "White") # Draw timer
    canvas.draw_text(str(player_correct) + "/" +str(num_stops),[450,25], 20, "Green") # Draw score
    
# create frame
frame = simplegui.create_frame("Stopwatch",500,500)

# register event handlers
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)
frame.set_draw_handler(draw_handler) 
# Draw handler updates frequently on its own
timer = simplegui.create_timer(100, tick)


# start frame
frame.start()

# Please remember to review the grading rubric
