########################################################################
# CSC 546 (Began Coding: 01/25/2019 11:20 PM | Due: 01/29/2019 5:59 PM)
#   Homework 2
#   2.0 Programming:
#       ii) For graduate students find a puzzle (the marble solitaire game
#           with 14 marbles is a fun one) or other problem of interest and 
#           code it up. Use either the BFS or the DFS to do this.
#               a) Extra Credit (5 points) – Also write a breadth-first search
#                   or explain thru complexity analysis of space and
#                   memory requirements due to depth and branching factor
#                   why it would not work on that problem.

# The following websites were referenced:
#   For understanding the game itself
#   https://en.wikipedia.org/wiki/Peg_solitaire
#
#   How to Implement Breadth-First Search in Python
#   https://pythoninwonderland.wordpress.com/2017/03/18/how-to-implement-breadth-first-search-in-python/
#
########################################################################

from random import shuffle # used to randomize the order in which moves are made
import queue # for Breadth-First-Search (BFS)

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
        self.gsParent = None

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
                    # for Row-Major order
#                    pegMoveFromTo = str(x+xDif+xDif) + ":" + str(y+yDif+yDif) + "-" + str(x) + ":" + str(y)
                    # for Column-Major order
                    pegMoveFromTo = str(y+yDif+yDif) + ":" + str(x+xDif+xDif) + "-" + str(y) + ":" + str(x)
                    changedState = True
                    return changedState, pegMoveFromTo, mCurrentState
    # No change to game state
    return changedState, pegMoveFromTo, mCurrentState

# Explore and create game space tree on-demand while traversing in BFS fashion
# Based on "BFS follows the following steps:"
#   1. Check the starting node 
#   2. Add its neighbours to the queue.
#   3. Mark the starting node as explored.
#   4. Get the first node from the queue / remove it from the queue
#   5. Check if node has already been visited.
#   6. If not, go through the neighbours of the node.
#   7. Add the neighbour nodes to the queue.
#   8. Mark the node as explored.
#   9. Loop through steps 4 to 8 until the queue is empty. (Note: Python won't recurse far enough)
#   https://pythoninwonderland.wordpress.com/2017/03/18/how-to-implement-breadth-first-search-in-python/
def BFS_PopulateGameSpaceTreeOnDemand():
    global mStartState

    # not initially used but still returned for now.
    solutionFound = False
    iterations = 0
    gsSolutionNode = None

    ##### Move 0 = Root: needed for gsMoveOne's parent
    gsMoveZero = GameSpaceNode("4:4", "StartState", 1, mStartState)

    ##### Move 1 = Singular Left Leaf
    # Insert first and only left node into Game Space Tree
    # Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
    stateChanged, movedFromTo, mNextState = AttemptStateChange(mStartState, "Diagonal_Down_Left")
    gsMoveOne = GameSpaceNode(movedFromTo, "Diagonal_Down_Left", 2, mNextState)
    gsMoveOne.gsParent = gsMoveZero

    # Create the unexploredQ and add the Singular Left Leaf to the unexploredQ
    unexploredQ = queue.Queue()

    # 1. Check the starting node (Unnecessary because it's the root)
    # 2. Add its neighbours to the queue.
    unexploredQ.put(gsMoveOne) # Add first child node as first unexplored
#    print(f"1: unexploredQ: {unexploredQ.qsize()}")

    while not solutionFound:
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
#                    print(f"iterations({iterations}): unexploredQ({unexploredQ.qsize()})")
                
                    score = GetScore(mNextState)

                    # 7. Add the neighbour nodes to the queue.
                    gsNewNode = GameSpaceNode(movedFromTo, dictMoveTypes[randomMoves[i]], score, mNextState)
                    gsNewNode.gsParent = gsDequeued
                    unexploredQ.put(gsNewNode)

                    if IsSolved(mNextState):
                        gsSolutionNode = gsNewNode
                        gsSolutionNode.solution = True
                        print(f"iterations({iterations}): unexploredQ({unexploredQ.qsize()})")
                        print("Solved:")
                        PrintState(mNextState)
                        print("--------------\n")
                        solutionFound = True

            # 8. Mark the node as explored.
            gsDequeued.explored = True

    return solutionFound, iterations, gsSolutionNode

def PrintBFSolution(SolutionWasFound, gsSolutionNode):
    if SolutionWasFound:
        print("The solution from last move to first")
        iterations = 0
        score = gsSolutionNode.score
        PrintState(gsSolutionNode.state)
        print(f"{gsSolutionNode.move} #{iterations}")
        iterations = iterations + 1
        gsParentNode = gsSolutionNode.gsParent
        PrintState(gsParentNode.state)
        print(f"{gsParentNode.move} #{iterations}")
        iterations = iterations + 1
        while score > 1 and iterations < 100:
            gsParentNode = gsParentNode.gsParent
            score = gsParentNode.score
            PrintState(gsParentNode.state)
            print(f"{gsParentNode.move} #{iterations}")
            iterations = iterations + 1

SolutionWasFound, NumberOfIterations, gsSolutionNode = BFS_PopulateGameSpaceTreeOnDemand()
print(f"The tree contains the solution? {SolutionWasFound}. It took {NumberOfIterations} iterations to discover using BFS.")

PrintBFSolution(SolutionWasFound, gsSolutionNode)
