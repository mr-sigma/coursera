"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        # create new grid visited which is the same size
        # as original grid
        visited = poc_grid.Grid(self.get_grid_height(), 
                                self.get_grid_width())
        visited.clear()
        
        # create 2D list distance_field same size as 
        # original grid and set entries to product of
        # width * height
        
        # need to change this from a grid to a 2D list
        distance_field = [[self.get_grid_height() * self.get_grid_width() \
                           for dummy_i in range(self.get_grid_width())] \
                          for dummy_j in range(self.get_grid_height())]
                                                
        
#        distance_field = poc_grid.Grid(self.get_grid_height(),
#                                       self.get_grid_width())
#        max_distance = distance_field.get_grid_height() * distance_field.get_grid_width()
#        for row in range(distance_field.get_grid_height()):
#            for col in range(distance_field.get_grid_width()):
#                distance_field[row][col] = max_distance
        
        # create a queue boundary that is a copy of the 
        # zombie list or human list based on entity_type
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            entity_list = self._zombie_list[:]
        elif entity_type == HUMAN:
            entity_list = self._human_list[:]
        else:
            print "Invalid entity_type"
            return
        
        for entity in entity_list:
            boundary.enqueue(entity)
            # initialize visited to be full at location
            visited.set_full(entity[0], entity[1])
            # set distance_field to be zero at location
            distance_field[entity[0]][entity[1]] = 0
        
        # BFS search
        while len(boundary) != 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor_cell in neighbors:
                if visited.is_empty(neighbor_cell[0], neighbor_cell[1]):
#                if neighbor_cell not in visited:
                    if self.is_empty(neighbor_cell[0], neighbor_cell[1]):
                        visited.set_full(neighbor_cell[0],
                                         neighbor_cell[1])
                        boundary.enqueue(neighbor_cell)
                        distance_field[neighbor_cell[0]][neighbor_cell[1]] = \
                        distance_field[current_cell[0]][current_cell[1]] + 1
                    
#        for row in distance_field:
#            print row
#        print 
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """

        for human in self.humans():
            # create list of neighboring cells
            # add current position in case it is the furthest from the zombies
            neighbors = self.eight_neighbors(human[0], human[1])
            neighbors.append(human)
            # neighbors in a list of tuples
            best_move = float('-inf')
            best_move_coord = ()
            # loop through neighbors and find the coordinates for the best move
            for (row, col) in neighbors:
                cur_move = zombie_distance_field[row][col]
                # take the best move
                if cur_move > best_move:
                    best_move = cur_move
                    best_move_coord = (row, col)
                # take a random choice of the moves if the moves have equal value
                elif cur_move == best_move:
                    best_move_coord = random.choice([best_move_coord, (row, col)])
                    
            index = self._human_list.index(human) 
            self._human_list[index] = best_move_coord
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in self.zombies():
            # add current position in case it is the furthest from the zombies
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            neighbors.append(zombie)
            # neighbors in a list of tuples
            best_move = float('inf')
            best_move_coord = ()
            # loop through neighbors and find the coordinates for the best move
            for (row, col) in neighbors:
                cur_move = human_distance_field[row][col]
                # take the best move
                if cur_move < best_move:
                    best_move = cur_move
                    best_move_coord = (row, col)
                # take a random choice of the moves if the moves have equal value
                elif cur_move == best_move:
                    best_move_coord = random.choice([best_move_coord, (row, col)])
                    
            index = self._zombie_list.index(zombie) 
            self._zombie_list[index] = best_move_coord

# Start up gui for simulation - You will need to write some code above
# before this will work without errors


# poc_zombie_gui.run_gui(Apocalypse(30, 40))

tst_zomb = [(0,0)]
tst_hum = [(10,10)]
poc_zombie_gui.run_gui(Apocalypse(30, 40, None, tst_zomb, tst_hum))
