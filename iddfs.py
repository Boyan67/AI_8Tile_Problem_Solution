import copy
import timeit

"""
Student number: 100280305
Name: Boyan Yonkov

This file containts my implementation of the Iterative Deepening Depth First search Algorithm
Results are output in the format: Depth: {-} Moves: {-} Time: {-}
"""

counter = 0


def increase_count(value):
    global counter
    counter += 1
    if value == 0:
        counter = 0

#Helper function for the main move function - adapted from the lectures
def move_blank(i, j, n):
    # down
    if i + 1 < n:
        increase_count(1)
        yield i + 1, j
    # up
    if i - 1 >= 0:
        increase_count(1)
        yield i - 1, j
    # right
    if j + 1 < n:
        increase_count(1)
        yield i, j + 1
    # left
    if j - 1 >= 0:
        increase_count(1)
        yield i, j - 1

#Function responsible for moving the tiles in the puzzel - adapted from the lectures
def move(state):
    copy_state = copy.deepcopy(state)
    [i, j, grid] = copy_state
    n = len(grid)
    for pos in move_blank(i, j, n):
        i1, j1 = pos
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]
        succ = [i1, j1, grid]
        yield succ
        grid[i][j], grid[i1][j1] = grid[i1][j1], grid[i][j]


#Helper function to check if current state is goal state
def is_goal(state, goal):
    return state == goal


#Recursive Depth First Search for one depth
def dfs_rec(path, depth, goal):
    if is_goal(path[-1], goal):
        return path
    if depth <= 0:
        return None
    else:
        for nextState in move(path[-1]):
            if nextState not in path:
                next_path = path + [nextState]
                solution = dfs_rec(next_path, depth - 1, goal)

                if solution is not None:
                    return solution
    return None

#Adding the Iterative Deepening part to the Depth First Search
#Calls dfs_rec as many times as needed to find solution
def iddfs(path, max_depth, goal):
    for depth in range(0, max_depth):
        result = dfs_rec([path], depth, goal)

        if result is None:
            continue
        return depth

    raise ValueError('goal not in graph with depth {}'.format(max_depth))

#Helper functon to show results
def run_iddfs(starting_state, goal):
    start_time = timeit.default_timer()
    depth = iddfs(starting_state, 50, goal)
    end_time = timeit.default_timer()
    time_taken = end_time - start_time
    print(f"Depth: {depth} Moves: {counter} Time: {time_taken}")


starting_states1 = [[0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]],
                    [0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]],
                    [2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]],
                    [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]],
                    [2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]],
                    ]
# Goal state
goal1 = [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]

starting_states2 = [[0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]],
                    [2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]],
                    [0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]],
                    [0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]],
                    [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]]
                    ]
# goal for starting states 2
goal2 = [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]


#For loops to show results from each of the strating states
for i in starting_states1:
    run_iddfs(i, goal1)
    increase_count(0)
    
for i in starting_states2:
    run_iddfs(i, goal2)
    increase_count(0)
