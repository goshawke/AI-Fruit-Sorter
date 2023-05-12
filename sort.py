import heapq
import math


class Fruit:
    def __init__(self, fruit_type, size):
        '''
        apple = 0, banana = 1. orange = 2
        '''
        self.type = fruit_type
        self.size = size

    def __lt__(self, other):
        return self.size < other.size

    def __gt__(self, other):
        return self.size > other.size

    def __repr__(self):
        return f"Fruit({self.type}, {self.size})"


# Sum of 4 parts
# Part 1: total number of inversions necessary to sort by type
# Part 2: the maximum between the total number of inversions necessary to sort BY SIZE for all rows AND the total number of inversions necessary to sort BY TYPE
# Part 3: the number of rows without each type (Apple, Banana, Orange) used
# Part 4: the maximum number of inversions required to fix bad rows (rows without all 3 types)
# (Part 4 may cause heurisitic to overestimate)
def heuristic(state):
    row_type_misplaced = 0
    col_j_size_misplaced = 0
    type_j_size_misplaced = 0
    for j in range(3):

        # All fruits belonging to Type j
        type_j_fruits = [
            fruit for col in state for fruit in col if fruit.type == j]
        
        col_fruit = []
        for col in state:
            col_fruit.append(col[j])
        
        inversions = 0
        for m in range(10):
            for n in range(m + 1, 10):
                if col_fruit[m] > col_fruit[n]:
                    inversions += 1

        col_j_size_misplaced += inversions


        inversions = 0
        for m in range(10):
            for n in range(m + 1, 10):
                if type_j_fruits[m] > type_j_fruits[n]:
                    inversions += 1

        type_j_size_misplaced += inversions

    # find number of type differences
    for i in range(10):

        # total number of inversions necessary to sort by type in a row
        for m in range(3):
            for n in range(m + 1, 3):

                if state[i][m].type > state[i][n].type:
                    row_type_misplaced += 1

    row_num = 0
    bad_rows = 0
    b_rows = []
    b_row_diff = 0
    types = [0, 1, 2]
    for row in state:
        used_types = set()
        for fruit in row:
            if fruit.type in types and fruit.type not in used_types:
                used_types.add(fruit.type)
            else:
                bad_rows += 1
                b_rows.append(row_num)
                #break

        row_num += 1
    if len(b_rows) >= 2:
        b_row_diff = abs(b_rows[0] - b_rows[-1])
        
    #distance = math.sqrt((type_misplaced)**2 + size_misplaced**2)

   #print(str(distance +  bad_rows))
    print('row type misplaced: ' + str(row_type_misplaced) +
          ', col size misplaced: ' + str(col_j_size_misplaced) +
          ', type size misplaced: ' + str(type_j_size_misplaced) +
           ', bad rows: ' + str(bad_rows) +
           ', bad rows diff: ' + str(b_row_diff/2))
        
    if col_j_size_misplaced >= type_j_size_misplaced:
        return row_type_misplaced + col_j_size_misplaced + bad_rows + (b_row_diff/2)
    else:
        return row_type_misplaced + type_j_size_misplaced + bad_rows + (b_row_diff/2)
    
   # return row_type_misplaced + max(col_j_size_misplaced + type_j_size_misplaced) + bad_rows #+ (b_row_diff/2)
# end of heuristic4()


# checks if the columns are all of the correct fruit type and if the heurisitic returns 0
def is_goal(state):
    for col in state:
        if (col[0].type != 0):
            return False
        if (col[1].type != 1):
            return False
        if (col[2].type != 2):
            return False
    return heuristic(state) == 0


def get_neighbors(state):
    neighbors = []
    for j in range(3):
        for i in range(10):

            if i < 9:
                # vertical swap
                new_state = [row.copy() for row in state]

                # pruning states that don't contribute to ordering size in ascending order
                new_state[i][j], new_state[i +
                                           1][j] = new_state[i+1][j], new_state[i][j]
                neighbors.append(new_state)

            if j < 2:
                # horizontal swap
                new_state = [row.copy() for row in state]

                # pruning states that don't contribute to ordering type in ascending order
                new_state[i][j], new_state[i][j +
                                              1] = new_state[i][j+1], new_state[i][j]
                neighbors.append(new_state)

    return neighbors


def a_star(initial_state):
    visited = set()
    # Add an empty list for the path
    queue = [(heuristic(initial_state), 0, initial_state, [])]
    while queue:
        _, cost, state, path = heapq.heappop(queue)
        state_tuple = tuple(tuple(f for f in row) for row in state)
        if state_tuple not in visited:
            visited.add(state_tuple)
            if is_goal(state):
                path.append(state)
                return cost, path  # Return the path along with the cost
            for neighbor in get_neighbors(state):
                new_path = path + [state]  # Add the current state to the path
                heapq.heappush(queue, (heuristic(neighbor) +
                               cost + 1, cost + 1, neighbor, new_path))
    return -1, []

# converges in < 10 seconds
# high lateral type displacement, No size displacement
initial_state1 = [
    [Fruit(0, 1), Fruit(1, 1), Fruit(2, 1)],
    [Fruit(1, 2), Fruit(2, 2), Fruit(0, 2)],
    [Fruit(2, 3), Fruit(0, 3), Fruit(1, 3)],
    [Fruit(0, 4), Fruit(1, 4), Fruit(2, 4)],
    [Fruit(1, 5), Fruit(2, 5), Fruit(0, 5)],
    [Fruit(2, 6), Fruit(0, 6), Fruit(1, 6)],
    [Fruit(0, 7), Fruit(1, 7), Fruit(2, 7)],
    [Fruit(1, 8), Fruit(2, 8), Fruit(0, 8)],
    [Fruit(2, 9), Fruit(0, 9), Fruit(1, 9)],
    [Fruit(0, 10), Fruit(1, 10), Fruit(2, 10)]
]

# converges in < 30 seconds
# no type displacement, high size displacement
initial_state2 = [
    [Fruit(0, 2), Fruit(1, 1), Fruit(2, 1)],
    [Fruit(0, 1), Fruit(1, 2), Fruit(2, 2)],
    [Fruit(0, 3), Fruit(1, 3), Fruit(2, 9)],
    [Fruit(0, 11), Fruit(1, 4), Fruit(2, 4)],
    [Fruit(0, 5), Fruit(1, 12), Fruit(2, 5)],
    [Fruit(0, 6), Fruit(1, 6), Fruit(2, 6)],
    [Fruit(0, 7), Fruit(1, 5), Fruit(2, 7)],
    [Fruit(0, 8), Fruit(1, 8), Fruit(2, 8)],
    [Fruit(0, 9), Fruit(1, 9), Fruit(2, 15)],
    [Fruit(0, 10), Fruit(1, 10), Fruit(2, 3)]
]

# converges in < 30 seconds
# high lateral type displacement, medium size displacement
initial_state3 = [
    [Fruit(0, 1), Fruit(1, 1), Fruit(2, 1)],
    [Fruit(1, 3), Fruit(2, 3), Fruit(0, 3)],
    [Fruit(2, 2), Fruit(0, 2), Fruit(1, 2)],
    [Fruit(0, 6), Fruit(1, 6), Fruit(2, 4)],
    [Fruit(1, 5), Fruit(2, 5), Fruit(0, 5)],
    [Fruit(2, 4), Fruit(0, 4), Fruit(1, 6)],
    [Fruit(0, 7), Fruit(1, 7), Fruit(2, 7)],
    [Fruit(1, 8), Fruit(2, 8), Fruit(0, 8)],
    [Fruit(2, 9), Fruit(0, 9), Fruit(1, 9)],
    [Fruit(0, 10), Fruit(1, 10), Fruit(2, 10)]
]

# Converges in < 2 minutes
# medium type displacement, high size displacement
initial_state4 = [
    [Fruit(1, 11), Fruit(0, 1), Fruit(2, 1)],
    [Fruit(0, 2), Fruit(1, 2), Fruit(2, 2)],
    [Fruit(2, 3), Fruit(1, 3), Fruit(0, 9)],
    [Fruit(0, 11), Fruit(1, 4), Fruit(2, 4)],
    [Fruit(1, 5), Fruit(0, 12), Fruit(2, 5)],
    [Fruit(0, 6), Fruit(1, 6), Fruit(2, 6)],
    [Fruit(0, 7), Fruit(1, 15), Fruit(2, 7)],
    [Fruit(0, 8), Fruit(1, 8), Fruit(2, 8)],
    [Fruit(0, 19), Fruit(1, 9), Fruit(2, 15)],
    [Fruit(0, 10), Fruit(1, 10), Fruit(2, 3)]
]

# Converges in < 30 secs
# type misplaced: 2, size misplaced: 25, bad rows: 2, bad rows diff: 1.0
initial_state5 = [
    [Fruit(0, 2), Fruit(1, 1), Fruit(2, 1)],
    [Fruit(0, 1), Fruit(1, 2), Fruit(2, 2)],
    [Fruit(2, 4), Fruit(1, 3), Fruit(2, 9)],
    [Fruit(0, 11), Fruit(1, 4), Fruit(2, 3)],
    [Fruit(0, 5), Fruit(1, 12), Fruit(0, 5)],
    [Fruit(0, 6), Fruit(1, 6), Fruit(2, 6)],
    [Fruit(0, 7), Fruit(1, 5), Fruit(2, 7)],
    [Fruit(0, 8), Fruit(1, 8), Fruit(2, 8)],
    [Fruit(0, 9), Fruit(1, 9), Fruit(2, 15)],
    [Fruit(0, 10), Fruit(1, 10), Fruit(2, 3)]
]

# converges in < 3 secs
# type misplaced: 0, size misplaced: 3, bad rows: 3, bad rows diff: 1.0
initial_state6 = [
    [Fruit(0, 2), Fruit(0, 1), Fruit(0, 1)],
    [Fruit(1, 1), Fruit(1, 2), Fruit(1, 2)],
    [Fruit(2, 3), Fruit(2, 3), Fruit(2, 4)],
    [Fruit(0, 4), Fruit(1, 4), Fruit(2, 4)],
    [Fruit(0, 5), Fruit(1, 5), Fruit(2, 5)],
    [Fruit(0, 6), Fruit(1, 6), Fruit(2, 6)],
    [Fruit(0, 7), Fruit(1, 5), Fruit(2, 7)],
    [Fruit(0, 8), Fruit(1, 8), Fruit(2, 8)],
    [Fruit(0, 9), Fruit(1, 9), Fruit(2, 9)],
    [Fruit(0, 10), Fruit(1, 10), Fruit(2, 10)]
]

# converges < 1 minute
# high lateral type displacement, No size displacement
initial_state7 = [
    [Fruit(0, 1), Fruit(1, 1), Fruit(2, 1)],
    [Fruit(1, 2), Fruit(2, 2), Fruit(0, 2)],
    [Fruit(0, 3), Fruit(0, 3), Fruit(1, 3)],
    [Fruit(0, 4), Fruit(1, 4), Fruit(2, 4)],
    [Fruit(1, 5), Fruit(2, 5), Fruit(2, 5)],
    [Fruit(2, 6), Fruit(0, 6), Fruit(1, 6)],
    [Fruit(0, 7), Fruit(1, 7), Fruit(2, 7)],
    [Fruit(2, 8), Fruit(2, 8), Fruit(0, 8)],
    [Fruit(2, 9), Fruit(0, 9), Fruit(1, 9)],
    [Fruit(0, 10), Fruit(1, 10), Fruit(1, 10)]
]




# Choose which initial_state is to be sorted here
cost, path = a_star(initial_state1)


# Prints the solution
print("Cost:", cost)
print("Path:")
for state in path:
    for row in state:
        row_text = ''
        for fruit in row:
            if fruit.type == 0:
                row_text += "(Apple, " + str(fruit.size) + ")  "
            elif fruit.type == 1:
                row_text += "(Banana, " + str(fruit.size) + ") "
            elif fruit.type == 2:
                row_text += "(Orange, " + str(fruit.size) + ") "
        print(row_text)
    print()

