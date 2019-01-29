######################################################
# CSC 546 (Began: 01/25/2019 11:20 PM)
#   Homework 2
#   2.0 Programming:
#       ii) For graduate students find a puzzle (the puzzle below is a fun
#           one) or other problem of interest and code it up. Use either the
#           BFS or the DFS to do this.
#               a) Extra Credit (5 points) – Also write a breadth-first search
#                   or explain thru complexity analysis of space and
#                   memory requirements due to depth and branching factor
#                   why it would not work on that problem.

# The following websites were referenced:
#   For understanding the game itself
#   https://en.wikipedia.org/wiki/Peg_solitaire
#
#   BFS & DFS matrix traversal code examples were helpful
#   https://towardsdatascience.com/depth-breath-first-search-matrix-traversal-in-python-with-interactive-code-back-to-basics-31f1eca46f55
#
#   Generate a graph using Dictionary in Python
#   https://www.geeksforgeeks.org/generate-graph-using-dictionary-python/
#   
######################################################

from random import shuffle # used to randomize the order in which moves are made
import queue # for Breadth-First-Search (BFS)
from collections import defaultdict # for Graph Path to prevent throwing errors for "key not found"

# Start state of game represented as a 9x9 matrix
mStartState =   [
                    [-1,-1,-1,-1,1,-1,-1,-1,-1]
                    , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    , [-1,-1,-1,1,-1,1,-1,-1,-1]
                    , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    , [-1,-1,1,-1,0,-1,1,-1,-1]
                    , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    , [-1,1,-1,1,-1,1,-1,1,-1]
                    , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    , [1,-1,1,-1,1,-1,1,-1,1]
                ]
# an individual node representing a specific game state
class GameSpaceNode: 
    def __init__(self, sMove, sMoveType, nSore, mState):
        self.explored = False
        self.solution = False
        self.move = sMove
        self.moveType = sMoveType
        self.score = nSore
        self.state = mState

    def __repr__(self):
        return {
            'move':self.move
            , 'moveType':self.moveType
            , 'score':self.score
        }
    
    def __str__(self):
        return "GameSpaceNode(solution=" + str(self.solution) + ", explored=" + str(self.explored) + ", move=" + self.move + ", moveType=" + self.moveType + ", score=" + str(self.score) + ")"

# deep-copy the given game state
def CopyState(mCurrentState):
    # initialized to all -1's
    mStateCopy =   [
                        [-1,-1,-1,-1,1,-1,-1,-1,-1]
                        , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                        , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                        , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                        , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                        , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                        , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                        , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                        , [-1,-1,-1,-1,-1,-1,-1,-1,-1]
                    ]
    for x in range(0, 9):
        for y in range(0, 9):
            mStateCopy[x][y] = mCurrentState[x][y]
    return mStateCopy

# Print the current game state as a pyramid:
#     1
#    1 1
#   1 0 1
#  1 1 1 1
# 1 1 1 1 1
def PrintState(mCurrentState):
    printed = False
    spacesToAdd = 4
    for x in range(0, 9):
        for y in range(0, 9):
            if mCurrentState[x][y] > -1:
                if spacesToAdd > 0 and printed == False:
                    print(f"{' ' * spacesToAdd}", end="")
                    spacesToAdd = spacesToAdd - 1
                print(f"{mCurrentState[x][y]}", end=" ")
                printed = True
        if printed:
            print("\n", end="")
            printed = False

# Check if the given game state is already solved
def IsSolved(mCurrentState):
    sum = 0
    for x in range(0, 9):
        for y in range(0, 9):
            if mCurrentState[x][y] > 0:
                sum = sum + 1
                if sum > 1:
                    return False
    if sum == 1:
        return True
    else:
        print(f"Warning: sum={sum} should never happen.")

# calculate the score of the given game state
def GetScore(mCurrentState):
    sum = 0
    for x in range(0, 9):
        for y in range(0, 9):
            if mCurrentState[x][y] == 0:
                sum = sum + 1
    if sum == 15:
        print(f"Warning: Score{sum} should never happen because 14 is the solution.")
    else:
        return sum

# Try to find a zero node that can be shifted according to the specified changeState
#   Note: Calling function must determine if game state was changed.
def AttemptStateChange(mActualState, changeType):
    # use a local variable to prevent changing the actual game state
    mCurrentState = CopyState(mActualState)
    changedState = False
    pegMoveFromTo = "N/A"
    xDif = 0
    yDif = 0
    # precalculate the necessary x,y moves to execute for all six possible moves
    # Note: the x & y moves are opposite than my original concept developed using Excel
    #   This must be because Python is traversing in Column-major instead of Row-major order
    if changeType == "Diagonal_Down_Left":
        xDif = xDif + 2
        yDif = yDif - 1
    elif changeType == "Diagonal_Down_Right":
        xDif = xDif + 2
        yDif = yDif + 1
    elif changeType == "Diagonal_Up_Left":
        xDif = xDif - 2
        yDif = yDif - 1
    elif changeType == "Diagonal_Up_Right":
        xDif = xDif - 2
        yDif = yDif + 1
    elif changeType == "Left":
        yDif = yDif - 2
    elif changeType == "Right":
        yDif = yDif + 2
    else:
        print(f"Warning: changeType({changeType}) should never happen")
  
#    print(f"Attempt {changeType} state change")
    # Game board is represented in a 9x9 matrix
    for x in range(0, 9):
        for y in range(0, 9):
            if mCurrentState[x][y] == 0:
                if ((x + xDif + xDif) < 9) and ((y + yDif + yDif) < 9) and mCurrentState[x+xDif][y+yDif] == 1 and mCurrentState[x+xDif+xDif][y+yDif+yDif] == 1:
#                    print(f"x{x},y{y} and {mCurrentState[x+xDif][y+yDif]} and {mCurrentState[x+xDif+xDif][y+yDif+yDif]}")
                    mCurrentState[x][y] = 1
                    mCurrentState[x+xDif][y+yDif] = 0
                    mCurrentState[x+xDif+xDif][y+yDif+yDif] = 0
                    pegMoveFromTo = str(x+xDif+xDif) + ":" + str(y+yDif+yDif) + "-" + str(x) + ":" + str(y)
                    changedState = True
                    return changedState, pegMoveFromTo, mCurrentState
    # No change to game state
    return changedState, pegMoveFromTo, mCurrentState

# First attempt at populating the entire game space tree as a matrix
# However, it does not preserver equal length rows, so it was not usable for subsequent
#   graph (as a matrix) traversals using BFS nor DFS
def PopulateGameSpaceTree(GameSpaceTree):
    global mStartState

    ##### Move 0 = Root
    # Insert root node into Game Space Tree
    # Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
    GameSpaceTree.append([]) # add an empty row 0
    GameSpaceTree[0].append(GameSpaceNode("Initial", "Static", 1, mStartState))

    ##### Move 1 = Singular Left Leaf
    # Insert first and only left node into Game Space Tree
    # Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
    stateChanged, movedFromTo, mNextState = AttemptStateChange(mStartState, "Diagonal_Down_Left")
    GameSpaceTree.append([]) # add an empty row 1
    GameSpaceTree[1].append(GameSpaceNode(movedFromTo, "Diagonal_Down_Left", 2, mNextState))

    dictMoveTypes = {
          0 : "Diagonal_Down_Left"
        , 1 : "Diagonal_Down_Right"
        , 2 : "Diagonal_Up_Left"
        , 3 : "Diagonal_Up_Right"
        , 4 : "Left"
        , 5 : "Right"
    }

    solutionFound = False
    iterations = 0
#    for row in range(2, 15):
    for row in range(2, 6):
        GameSpaceTree.append([]) # add an empty row 0
        for col in range(0, len(GameSpaceTree[row-1])):
            mCurrentState = GameSpaceTree[row-1][col].state
#            print(GameSpaceTree[row-1][col])
#            PrintState(mCurrentState)
            # randomize the oder in which moves are attempted
            randomMoves = [0,1,2,3,4,5]
            shuffle(randomMoves)
            for i in range(0, 6):
                stateChanged, movedFromTo, mNextState = AttemptStateChange(mCurrentState, dictMoveTypes[randomMoves[i]])
                if stateChanged:
                    iterations = iterations + 1
                    score = GetScore(mNextState)
                    if row != score - 1:
                        print(f"Warning: {row} != {scroe - 1} should never happen")
                    GameSpaceTree[score-1].append(GameSpaceNode(movedFromTo, dictMoveTypes[randomMoves[i]], score, mNextState))
                    if IsSolved(mNextState):
                        print("Solved:")
                        PrintState(mNextState)
                        solutionFound = True
                        return solutionFound, iterations
    return solutionFound, iterations
#               else:
#                   print(f"Unable to move {randomMoves[i]} = {dictMoveTypes[randomMoves[i]]}")

# A subsequent attempt to populate the entire game space tree by augmenting the above
# function PopulateGameSpaceTree() to simultaneously populate a Python dictionary to represent
# keys as nodes and associated values as a list of the node's connected edges 
def PopulateGameSpaceTreeAndEdges(GameSpaceTree, dictGameSpaceEdges):
    global mStartState

    ##### Move 0 = Root
    # Insert root node into Game Space Tree
    # Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
    GameSpaceTree.append([]) # add an empty row 0
    GameSpaceTree[0].append(GameSpaceNode("4:4", "Static", 1, mStartState))

#    dictGameSpaceEdges["4:4"] = ["root"]

    ##### Move 1 = Singular Left Leaf
    # Insert first and only left node into Game Space Tree
    # Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
    stateChanged, movedFromTo, mNextState = AttemptStateChange(mStartState, "Diagonal_Down_Left")
    GameSpaceTree.append([]) # add an empty row 1
    GameSpaceTree[1].append(GameSpaceNode(movedFromTo, "Diagonal_Down_Left", 2, mNextState))

    dictGameSpaceEdges["4:4"] = [movedFromTo]

    dictMoveTypes = {
          0 : "Diagonal_Down_Left"
        , 1 : "Diagonal_Down_Right"
        , 2 : "Diagonal_Up_Left"
        , 3 : "Diagonal_Up_Right"
        , 4 : "Left"
        , 5 : "Right"
    }

    solutionFound = False
    iterations = 0
#    for row in range(2, 15):
    for row in range(2, 6):
        GameSpaceTree.append([]) # add an empty row 0
        for col in range(0, len(GameSpaceTree[row-1])):
            mCurrentState = GameSpaceTree[row-1][col].state
            mCurrentMove = GameSpaceTree[row-1][col].move
#            print(GameSpaceTree[row-1][col])
#            PrintState(mCurrentState)
            # randomize the oder in which moves are attempted
            randomMoves = [0,1,2,3,4,5]
            shuffle(randomMoves)
            for i in range(0, 6):
                stateChanged, movedFromTo, mNextState = AttemptStateChange(mCurrentState, dictMoveTypes[randomMoves[i]])
                if stateChanged:
                    iterations = iterations + 1
                    score = GetScore(mNextState)
                    if row != score - 1:
                        print(f"Warning: {row} != {scroe - 1} should never happen")
                    GameSpaceTree[score-1].append(GameSpaceNode(movedFromTo, dictMoveTypes[randomMoves[i]], score, mNextState))
                    # add path
                    if dictGameSpaceEdges[mCurrentMove] is None:
                        dictGameSpaceEdges[mCurrentMove] = [movedFromTo]
                    else:
                        dictGameSpaceEdges[mCurrentMove] += [movedFromTo]

                    if IsSolved(mNextState):
                        print("Solved:")
                        PrintState(mNextState)
                        solutionFound = True
                        return solutionFound, iterations
    return solutionFound, iterations

# First attempt to traverse the matrix created by PopulateGameSpaceTree() which proved unsuccessful
# Based on "BFS follows the following steps:"
#   1. Check the starting node and add its neighbours to the queue.
#   2. Mark the starting node as explored.
#   3. Get the first node from the queue / remove it from the queue
#   4. Check if node has already been visited.
#   5. If not, go through the neighbours of the node.
#   6. Add the neighbour nodes to the queue.
#   7. Mark the node as explored.
#   8. Loop through steps 3 to 7 until the queue is empty.
#   https://pythoninwonderland.wordpress.com/2017/03/18/how-to-implement-breadth-first-search-in-python/
def MatrixBFS(unexploredQ):
    global GameSpaceTree

    print("Begin MatrixBFS")
    print(f"unexploredQ=({unexploredQ})")
    # 3. Get the first node from the queue / remove it from the queue
    current_index = unexploredQ.get()
    current_x, current_y = current_index[0], current_index[1]
    print(f"current_index = {current_index}")

    if current_x != 0 and current_x != 0:
        print("unexploredQ is not empty")
        # 1.a Check the current dequeued node...
#        if GameSpaceTree[current_x][current_y].score == 14:
        if GameSpaceTree[current_x][current_y].score == 4:
            return current_x, current_y
        # 4. Check if node has already been visited.
        if GameSpaceTree[current_x][current_y].explored == False:
            # 5. If not, go through the neighbours of the node.
            for col in range(current_y, len(GameSpaceTree[current_x+1])):
                # 6. Add the neighbour nodes to the queue.
                unexploredQ.put((current_x+1,col))
                print(f"[{current_x+1}][{col}] = {GameSpaceTree[current_x+1][col]}")
            # 7. Mark the node as explored.
            GameSpaceTree[current_x][current_y].explored = True
            print(f"1: unexploredQ: {unexploredQ.qsize()}")
    else:
        print("unexploredQ is empty")
        # 1.a Check the starting node...
        if GameSpaceTree[0][0].score == 14:
            return 0, 0
        for col in range(0, len(GameSpaceTree[1])):
            # 1.b ...and add starting node's neighbours to the queue.
            unexploredQ.put((1,col))
            print(f"[{0}][{col}] = {GameSpaceTree[0][col]}")
        # 2. Mark the starting node as explored.
        GameSpaceTree[0][0].explored = True
        print(f"2: unexploredQ: {unexploredQ.qsize()}")
    
    return MatrixBFS(unexploredQ)
#    return unexploredQ

# Attempt to build the graph's edge dictionary on-demand while traversing in BFS fashion
# Example dictionary entry: '2:5-6:3': ['8:6-8:2', '6:7-2:5'].
# Note: verticies are labled by the move (i.e., '2:5-6:3') that brought them into their 
#   current game state
# Note: The first node in every edge list is the identical to the dictionary entry's key
# Again, based on "BFS follows the following steps:"
#   1. Check the starting node 
#   2. Add its neighbours to the queue.
#   3. Mark the starting node as explored.
#   4. Get the first node from the queue / remove it from the queue
#   5. Check if node has already been visited.
#   6. If not, go through the neighbours of the node.
#   7. Add the neighbour nodes to the queue.
#   8. Mark the node as explored.
#   9. Loop through steps 4 to 8 until the queue is empty. (Note: Python won't recurse far enough)
def BFS_PopulateGameSpaceTreeEdgesOnDemand(dictGameSpaceEdges):
    global mStartState

    # not initially used but still returned for now.
    solutionFound = False
    iterations = 0
    duplicateWarnings = 0

    ##### Move 0 = Root: ignored because the root has only one child node

    ##### Move 1 = Singular Left Leaf
    # Insert first and only left node into Game Space Tree
    # Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
    stateChanged, movedFromTo, mNextState = AttemptStateChange(mStartState, "Diagonal_Down_Left")
    gsMoveOne = GameSpaceNode(movedFromTo, "Diagonal_Down_Left", 2, mNextState)
    dictGameSpaceEdges[movedFromTo] = [gsMoveOne]

    # Create the unexploredQ and add the Singular Left Leaf to the unexploredQ
    unexploredQ = queue.Queue()

    # 1. Check the starting node (Unnecessary because it's the root)
    # 2. Add its neighbours to the queue.
    unexploredQ.put(gsMoveOne) # Add first child node as first unexplored
    print(f"1: unexploredQ: {unexploredQ.qsize()}")

    while not solutionFound and duplicateWarnings < 10:
        # 4. Get the first node from the queue / remove it from the queue
        gsDequeued = unexploredQ.get()
    #    print(f"1: unexploredQ:{unexploredQ.qsize()} move={gsDequeued.move}")

        # 5. Check if node has already been visited.
        if not gsDequeued.explored:

            dictMoveTypes = {
                0 : "Diagonal_Down_Left"
                , 1 : "Diagonal_Down_Right"
                , 2 : "Diagonal_Up_Left"
                , 3 : "Diagonal_Up_Right"
                , 4 : "Left"
                , 5 : "Right"
            }

    #        print(gsDequeued)
    #        PrintState(gsDequeued.state)

            # randomize the oder in which moves are attempted
            randomMoves = [0,1,2,3,4,5]
            shuffle(randomMoves)
            for i in range(0, 6):
                stateChanged, movedFromTo, mNextState = AttemptStateChange(gsDequeued.state, dictMoveTypes[randomMoves[i]])
                if stateChanged:
                    iterations = iterations + 1
                    print(f"iterations({iterations}): unexploredQ({unexploredQ.qsize()})")
                
                    score = GetScore(mNextState)

                    # 7. Add the neighbour nodes to the queue.
                    gsNewNode = GameSpaceNode(movedFromTo, dictMoveTypes[randomMoves[i]], score, mNextState)
                    unexploredQ.put(gsNewNode)

                    # Add all neibour nodes to the edge dictionary
                    if dictGameSpaceEdges[gsDequeued.move] is None:
                        dictGameSpaceEdges[gsDequeued.move] = [gsNewNode]
#                        dictGameSpaceEdges[gsDequeued.move] = [gsDequeued, gsNewNode]
                    elif gsDequeued.move != gsNewNode.move:
                        dictGameSpaceEdges[gsDequeued.move] += [gsNewNode]
                    else:
                        print("Error: duplicate moves: {gsDequeued.move} == {gsNewNode.move}")
                        duplicateWarnings = duplicateWarnings + 1

                    if IsSolved(mNextState):
                        gsNewNode.solution = True
                        print("Solved:")
                        PrintState(mNextState)
                        solutionFound = True
                        return solutionFound

            # 8. Mark the node as explored.
            gsDequeued.explored = True

    # return as yet to be decided
    return solutionFound, iterations


# 2D matrix where rows are of equal game scores and columns are increasing game scores
GameSpaceTree = []

dictGameSpaceEdges = defaultdict(list)

BFS_PopulateGameSpaceTreeEdgesOnDemand(dictGameSpaceEdges)

solutionKey = ""
stepsToSolution = 0
count = 0
for key in dictGameSpaceEdges.keys():
    print(f"key1={key}")
    count = 0
    for i in range(0, len(dictGameSpaceEdges[key])):
        count = count + 1
        if dictGameSpaceEdges[key][i].solution:
            solutionKey = key
            stepsToSolution = count
            print(f"move={dictGameSpaceEdges[key][i].move} sol={str(dictGameSpaceEdges[key][i].solution)}", end=" ")
        else:
            print(f"move={dictGameSpaceEdges[key][i].move}", end=" ")
    print("\n")

# print solution
print(f"key={solutionKey} contains the {stepsToSolution} moves leading to the solution")
for i in range(0, len(dictGameSpaceEdges[solutionKey]) ):
    PrintState(dictGameSpaceEdges[solutionKey][i].state)
    if dictGameSpaceEdges[solutionKey][i].solution:
        print(f"move={dictGameSpaceEdges[solutionKey][i].move} sol={str(dictGameSpaceEdges[solutionKey][i].solution)}")
    else:
        print(f"move={dictGameSpaceEdges[solutionKey][i].move}")


# dictGameSpaceEdges['a:b'] = ["a"]
# if dictGameSpaceEdges['a:b'] is None:
#     dictGameSpaceEdges['a:b'] = ["b"]
# else:
#     dictGameSpaceEdges['a:b'] += ["b"]
# print(dictGameSpaceEdges['a:b'])

########################################################
##### Test dictionary storage of GameStateNodes & Q
def TestDictOfEdges():
    global mStartState

    gsOne = GameSpaceNode("Initial", "Static", 1, mStartState)
    gsTwo = GameSpaceNode("Next", "Diagonal_Down_Left", 2, mStartState)

    dictGameSpaceEdges['a:b'] = [gsOne]
    if dictGameSpaceEdges['a:b'] is None:
        dictGameSpaceEdges['a:b'] = [gsTwo]
    else:
        dictGameSpaceEdges['a:b'] += [gsTwo]
    #print( list( dictGameSpaceEdges.items() )[0][1].score)
    print(list(dictGameSpaceEdges.keys()))
    print(f"len={len(dictGameSpaceEdges['a:b'])}")

    unexploredQ = queue.Queue()

    for key in dictGameSpaceEdges.keys():
        print(f"key={key}")
        for i in range(0, len(dictGameSpaceEdges[key]) ):
            unexploredQ.put(dictGameSpaceEdges[key][i])
            print(f"score={dictGameSpaceEdges[key][i].score}")

    gsDequeued = unexploredQ.get()
    print(f"1: unexploredQ:{unexploredQ.qsize()} move={gsDequeued.move}")
#TestDictOfEdges()
########################################################

# SolutionWasFound, NumberOfIterations = PopulateGameSpaceTreeAndEdges(GameSpaceTree, dictGameSpaceEdges)
# print(dictGameSpaceEdges)

#SolutionWasFound, NumberOfIterations = PopulateGameSpaceTree(GameSpaceTree)
# print(f"The tree contains the solution? {SolutionWasFound}. It took {NumberOfIterations} iterations.")

# Note: requires PopulateGameSpaceTree() to have been executed first
def PrintGameSpaceTree(GameSpaceTree):
    rows = len(GameSpaceTree)
    for r in range(0, rows):
        for c in range(0, len(GameSpaceTree[r])):
#            print(f"[{r}][{c}] = {GameSpaceTree[r][c]}")
            print(f"[{r}][{c}]", end=" ")
        print("\n")

# Note: requires PopulateGameSpaceTree() to have been executed first
def PrintGameSpaceTreeBranchingFactors(GameSpaceTree):
    totalNodes = 0
    rows = len(GameSpaceTree)
    for r in range(0, rows):
        totalNodes = totalNodes + len(GameSpaceTree[r])
        print(f"Row[{r}]\t has {str(len(GameSpaceTree[r]))} nodes")
    print(f"For a total of {totalNodes} nodes")

#PrintGameSpaceTreeBranchingFactors(GameSpaceTree)

#####################################################
############# Reference External Code ###############
# This code requires numpy and is only here as reference
#####################################################

#PrintGameSpaceTree(GameSpaceTree)

# 4. Queue for BFS
#start_queue = queue.Queue()
#start_queue.put((0,0))
#BFS_results = BFS(start_queue)

#start_queue = queue.Queue()
#start_queue.put((0,0))
#MatrixBFS(start_queue)
#print(f"[{0}][{0}] = {GameSpaceTree[0][0]}")
#print(f"Results of BFS = {BFS_results}")
