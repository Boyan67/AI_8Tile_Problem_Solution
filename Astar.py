from copy import deepcopy
import timeit

"""
Student number: 100280305
Name: Boyan Yonkov

This file containts my implementation of the A* algorithm to solve the 8-tile problem
Results are output in the format: Depth: {-} Moves: {-} Time: {-}
"""

counter = 0


def increase_count(value):
    global counter
    counter += 1
    if value == 0:
        counter = 0

states_list_num = 1


# First Set of Starting States
starting_states1 = [[0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]],
                    [0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]],
                    [2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]],
                    [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]],
                    [2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]],
                    ]

#Second Set of Starting States
starting_states2 = [[0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]],
                    [2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]],
                    [0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]],
                    [0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]],
                    [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]
                    ]

# Goal state for First Set of Starting States
goal = [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]


#A helper function that converts a state into a dictionary
#This allows me to be able to calculate the manhattand distance
def make_dict(state):
    coordinate_dict = {}
    for x, row in enumerate(state):
        for y, value in enumerate(row):
            coordinate_dict[value] = (x, y)
    return coordinate_dict


#Class to create 8-puzzel objects
#Use: get manhattan distance and check if goal state is reached
class puzzle:
    def __init__(self, starting, parent):
        self.board = starting
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def manhattan(self):
        dict_start = make_dict(self.board[2])
        dict_goal = make_dict(goal[2])
        distance = 0
        for i in range(1, len(dict_goal)):
            distance += abs(dict_goal[i][0] - dict_start[i][0]) + abs(dict_goal[i][1] - dict_start[i][1])
        return distance

    def goal(self):
        return self.board == goal

    def __eq__(self, other):
        return self.board == other.board

#Move function to handle moving the tiles
def move_func(state):
    curr = state.board
    [i, j, grid] = curr
    n = len(grid)

    if i + 1 < n:
        [i, j, grid] = deepcopy(curr)
        grid[i][j], grid[i + 1][j] = grid[i + 1][j], grid[i][j]
        b = [i + 1, j, grid]
        increase_count(1)
        yield puzzle(b, curr)

    # up
    if i - 1 >= 0:
        [i, j, grid] = deepcopy(curr)
        grid[i][j], grid[i - 1][j] = grid[i - 1][j], grid[i][j]
        b = [i - 1, j, grid]
        increase_count(1)
        yield puzzle(b, curr)

    # right
    if j + 1 < n:
        [i, j, grid] = deepcopy(curr)
        grid[i][j], grid[i][j + 1] = grid[i][j + 1], grid[i][j]
        b = [i, j + 1, grid]
        increase_count(1)
        yield puzzle(b, curr)
    # left
    if j - 1 >= 0:
        [i, j, grid] = deepcopy(curr)
        grid[i][j], grid[i][j - 1] = grid[i][j - 1], grid[i][j]
        b = [i, j - 1, grid]
        increase_count(1)
        yield puzzle(b, curr)


# Function to calculate f() from the a*algorithm in lectures 
def best_f_value(open_list):
    f = open_list[0].f
    index = 0
    for i, item in enumerate(open_list):
        if i == 0:
            continue
        if (item.f < f):
            f = item.f
            index = i

    return open_list[index], index

#The A* algorithm
def a_start(start):
    depth = 0
    
    open_list = []
    closed_list = []
    open_list.append(start)

    while open_list:
        current, index = best_f_value(open_list)
        
        if current.board == goal:
            
            return current, depth
        
        open_list.pop(index)
        closed_list.append(current)

        X = move_func(current)
        for move in X:
            ok = False
            for i, item in enumerate(closed_list):
                if item == move:
                    ok = True
                    break
            if not ok:
                newG = current.g + 1
                present = False

                for j, item in enumerate(open_list):

                    if item == move:
                        present = True
                        
                        if newG < open_list[j].g:
                            open_list[j].g = newG
                            open_list[j].f = open_list[j].g + open_list[j].h
                            open_list[j].parent = current
                            
                if not present:
                    move.g = newG
                    depth = move.g
                    move.h = move.manhattan()
                    move.f = move.g + move.h
                    move.parent = current
                    open_list.append(move)
    
    return None


#Loops to show the results from running the A* algorithm 
for i in starting_states1:
    start = puzzle(i, None)
    start_time = timeit.default_timer()
    result, depth = a_start(start)
    end_time = timeit.default_timer()
    time_taken = end_time - start_time
    print(f"Depth: {depth} Moves: {counter} Time: {time_taken}")
    increase_count(0)

# Goal state for Second Set of Starting States
goal = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]

print("SECOND GOAL")
for i in starting_states2:
    start = puzzle(i, None)
    start_time = timeit.default_timer()
    result, depth = a_start(start)
    end_time = timeit.default_timer()
    time_taken = end_time - start_time
    print(f"Depth: {depth} Moves: {counter} Time: {time_taken}")
    increase_count(0)


    
