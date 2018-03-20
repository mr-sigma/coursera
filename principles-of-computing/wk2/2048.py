"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Modify URL as necessary
# import user41_2e3kTq5KJb8Inkz_6 as tests

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # make sure the grid is more than one element
    # else return the original gird
    if len(line) < 2:
        return line
    slide_line = slide(line)
    for i_dummy in range(len(slide_line) - 1):
        try:
            if slide_line[i_dummy] == 0:
                continue
            # if adjacent tiles are equal, combine
            # them and zero out the further of the two
            if slide_line[i_dummy] == slide_line[i_dummy+1]:
                slide_line[i_dummy] *= 2
                slide_line[i_dummy+1] = 0
                continue
        except IndexError:
            continue
    # trim zeroes from the list and return the value            
    return slide(slide_line)

def slide(lst):
    """
    Function to slide over numbers in a list
    Trims zero entries and puts them at the end
    of the list
    """
    slide_line = [x for x in lst if x != 0]
    while len(slide_line) < len(lst):
        slide_line.append(0)
    return slide_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width   
        self._anchor_tiles = {
            UP: [(0,x) for x in range(self._grid_width)],
            DOWN: [(self._grid_height - 1,x) for x in range(self._grid_width)],
            LEFT: [(x,0) for x in range(self._grid_height)],
            RIGHT: [(x,self._grid_width - 1) for x in range(self._grid_height)]
        }
        self._full = False
        # Create an empty board and place two
        # blocks on the board
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_j in range(self._grid_width)]
                     for dummy_i in range(self._grid_height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        to_return = ""
        for dummy in self._grid:
            to_return += str(dummy) + "\n"
        return to_return

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        row_off = OFFSETS[direction][0]
        col_off = OFFSETS[direction][1]
        loop = {
            UP: self._grid_height,
            DOWN: self._grid_height,
            LEFT: self._grid_width,
            RIGHT: self._grid_width
        }
        # pick an anchor tile based on direction
        for entry in self._anchor_tiles[direction]:
            temp_list = []
            index = []
            row = entry[0]
            col = entry[1]
            # iterate through the grid to create a list to pass to merge
            for i_dummy in range(loop[direction]):
                try:
                    # calculate the incrementation 
                    # to the anchor tile indices
                    row_incre = i_dummy * row_off
                    col_incre = i_dummy * col_off
                    # append values to temp lists
                    temp_list.append(
                        self._grid[row + row_incre][col + col_incre]
                    )
                    index.append((row + row_incre, col + col_incre))
                except IndexError:
                    continue
                # check to see if any tiles were moved
                new_list = merge(temp_list)
                if new_list != temp_list:
                    moved = True
                if 2048 in new_list:
                    print "You've Won!!!"
                # overwrite the tiles in the grid
                for i_dummy in range(len(new_list)):
                    self.set_tile(index[i_dummy][0], index[i_dummy][1], new_list[i_dummy])
                
        if moved:
            self.new_tile()

    def rand_coord(self):
        """
        Generates a pair of random indicies within the 
        confines of the grid and returns them as 
        row, col
        """
        row = random.randrange(0, self._grid_height)
        col = random.randrange(0, self._grid_width)
        return row, col
    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        
        Return: 
            True if grid full
            False if grid has space
        
        Will toggle self._full variable if there is no where left to put the
        tile
        """
        
        # set an initial random coordinate
        row, col = self.rand_coord()
        # while the randomly selected cell is not empty
        # keep assigning new indicies
        count = 0
        while self._grid[row][col] != 0:
            # set a break condition
            if count > 10000:
                self._full = True
                return True
            row, col = self.rand_coord()
            count += 1

        # create a random number that puts 
        # a 2 or 4 in an empty cell
        num = random.randrange(1,100)
        if num < 90:
            # set the tile to 2 90% of the time
            self.set_tile(row, col, 2)
        else:
            # set the tile to 4 10% of the time
            self.set_tile(row, col, 4)
        return False

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

# define grid here
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
