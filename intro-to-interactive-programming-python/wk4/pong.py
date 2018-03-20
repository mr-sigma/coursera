# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [300, 200] # center of the canvas
ball_vel = [random.randrange(120, 240), random.randrange(60, 180)]
paddle1_pos = 200 # center of canvas
paddle2_pos = 200 # center of canvas
paddle1_vel = 0
paddle2_vel = 0
vel_constant = 8
score1 = score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [300, 200] # center of the canvas
    
    # multiplied by -1 to get the ball to travel up
    ball_vel[1] = -1 * random.randrange(60, 180)/60
    
    # divide by 60 to match the refresh rate of the draw handler
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240)/60
    elif direction == LEFT:
        ball_vel[0] = -1 * random.randrange(120, 240)/60
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = 200 # center of canvas
    paddle2_pos = 200 # center of canvas
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(random.randint(0,1))
    score1 = score2 = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global BALL_RADIUS
    

    
    
    
    # will bounce off top wall
    if (ball_pos[1] + BALL_RADIUS > HEIGHT) or (ball_pos[1] - BALL_RADIUS < 0):
        ball_vel[1] *= -1
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]    
    # check that the ball is touching the paddle (ball center within the range of paddle)
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 12, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    if (paddle1_pos + HALF_PAD_HEIGHT > HEIGHT):
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    elif (paddle1_pos - HALF_PAD_HEIGHT < 0):
        paddle1_pos = HALF_PAD_HEIGHT
    if (paddle2_pos + HALF_PAD_HEIGHT > HEIGHT):
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    elif (paddle2_pos - HALF_PAD_HEIGHT < 0):
        paddle2_pos = HALF_PAD_HEIGHT

    
    #------------------ draw paddles
    
    # paddle 1
    canvas.draw_polygon([[0, paddle1_pos + HALF_PAD_HEIGHT], # upper left 1
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], # upper right 1
                         [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], # bottom right 1
                         [0, paddle1_pos - HALF_PAD_HEIGHT]], # bottom left 1
                         0.25, 'White', "White")
    # canvas.draw_polygon([[30, 20], [40, 40], [50, 20], [10, 10]], 12, 'Red')
    # paddle 2
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], # upper left 2
                         [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], # upper right 2
                         [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], # bottom right 2
                         [WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT]], # bottom left 2
                         0.25, 'White', "White")
    
    # determine whether paddle and ball collide    
    
    # check that the ball touches the gutter area
    # then spawn heading the other direction
    if (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH): # Ball touching right wall
        if ball_pos[1] in range(paddle2_pos - HALF_PAD_HEIGHT - BALL_RADIUS - 1, 
                                paddle2_pos + HALF_PAD_HEIGHT + BALL_RADIUS + 1):
            ball_vel[0] *= -1.1 # increase speed by 10%
        else:
            score1 += 1
            spawn_ball(LEFT) # spawn ball towards other wall
    elif (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH): # Ball touching left wall
        if ball_pos[1] in range(paddle1_pos - HALF_PAD_HEIGHT - BALL_RADIUS + 1, 
                                paddle1_pos + HALF_PAD_HEIGHT + BALL_RADIUS + 1 ):
            ball_vel[0] *= -1.1 # increase speed by 10%
        else:
            score2 += 1
            spawn_ball(RIGHT) # spawn ball towards other wall
    
    # draw scores
    canvas.draw_text(str(score1),[30,30],30,"White")
    canvas.draw_text(str(score2),[WIDTH - 30,30],30,"White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -vel_constant # paddle 1 moves up
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel_constant # paddle 1 moves down
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -vel_constant
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel_constant
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)


# start frame
new_game()
frame.start()
