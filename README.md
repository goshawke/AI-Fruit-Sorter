# AI-Fruit-Sorter
PROBLEM
--------
You are given 10 apples of different sizes, 10 bananas of different sizes, and 10 oranges of different sizes, organized in a 3x10 array.
Each element has a type (apple, banana, or orange) and a size (integer). You want to organize them by type and by size.
Firstly, they must be organized so that all apples are in the first column, all bananas are in the second column, and all oranges are in the third column.
Secondly, the elements of each type must be organized within their column in ascending order based on size. The only move allowed is to swap two fruits horizontally or vertically.
You want to use A* algorithm to minimize the number of moves for this. 

APPROACH
---------
To use the A* algorithm to minimize the number of moves required to sort the fruits according to type and in ascending order of size.

Algorithm Implementation: A priority queue to store the states, sorted by heuristic + cost

Fruit Representation: A tuple containing of type Fruit. A Fruit has an integer type = [0,1,2] and integer size. type of 1 is Apple, 2 is Banana, 3 is Orange
    - Fruit(0, #), Fruit(1, #), or Fruit(2, #)

State: A state is defined as the current arrangement of fruits in the 3x10 array.
    - 3x10 list of tuples, where each integer represents the size of a fruit

Goal State: An arrangement of Fruits within the 3x10 array so that: 
    1. Column 0 contains only fruit of type 0 (Apple), column 1 contains only fruit of type 1 (Banana), and column 2 contains only fruit of type 2 (Orange)
    2. The fruit within each column are sorted in ascending order based on their Fruit.size value
    3. The fruit within each row are sorted in ascending order based on their Fruit.type value

Action Space: the set of all possible swaps of adjacent fruits, either horizontally or vertically.

Actions: An action is defined as swapping two fruits horizontally or vertically.
    - We can define four types of actions: move left, move right, move up, and move down. 
        - For example, if we want to swap the fruit in position (1,1) with the fruit in position (2,1), we can apply the move down action.

Cost: The cost of an action is defined as the number of moves required to perform the action.
    - The cost of an action is 1, since each swap requires one move.

Heuristic: Sum of 4 Parts
    1. Total number of inversions (swaps) necessary to sort by type
    2. The maximum between the total number of inversions necessary to sort BY SIZE for all rows AND the total number of inversions necessary to sort BY TYPE
    3. The number of rows without each type (Apple, Banana, Orange) used
    4. The maximum number of inversions required to fix bad rows (rows without all 3 types)
(Part 4 may cause heurisitic to overestimate)Total steps (swaps) required to arrange a column in ascending order based on Fruit.size


