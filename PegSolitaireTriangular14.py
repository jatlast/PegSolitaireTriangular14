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
#
# Note: this code is available on GitHub 
#   https://github.com/jatlast/PegSolitaireTriangular14
#
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

# Note: Only BFS (working) or DFS (finds multiple solutions) can be run at a time
#   I realize the below should be command line options, but, I'm out of time.
versionToRun = "BFS"    # Prints only the optimal solution as output
#versionToRun = "DFS"   # Prints 2.3 Mb and the first solution as output (search for "Solved")
# DFS Note: Storing all the solutions then picking the shortest would probably work,
#   however, I am out of time on this homework assignment.

##########################
#### Global Variables ####
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

# move from the perspective of the empty hole
dictMoveTypes = {
    0 : "Diagonal_Down_Left"
    , 1 : "Diagonal_Down_Right"
    , 2 : "Diagonal_Up_Left"
    , 3 : "Diagonal_Up_Right"
    , 4 : "Left"
    , 5 : "Right"
}
##########################

############################## Shared DFS/BFS Code ##############################

# an individual node representing a specific game state
class GameSpaceNode: 
    def __init__(self, sMove, sMoveType, nSore, mState):
        self.move = sMove
        self.moveType = sMoveType
        self.score = nSore
        self.state = mState
        self.explored = False   # used for DFS visited & BFS explored
        self.processed = False  # used for DFS processed
        self.solution = False
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

############################## BFS Code ##############################

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
    global dictMoveTypes

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
                        print("Solved:")
                        PrintState(mNextState)
                        print("--------------\n")
                        solutionFound = True

            # 8. Mark the node as explored.
            gsDequeued.explored = True

    print(f"iterations({iterations}): unexploredQ({unexploredQ.qsize()})")
    return solutionFound, iterations, gsSolutionNode

def PrintBFSolution(SolutionWasFound, gsSolutionNode):
    print("----- Optimal BFS Solution -----")
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

########################
### BFS driving code ###
# Note: Only DFS or BFS can be run at a time
if versionToRun == "BFS":
    print("----- BFS Output -----")
    SolutionWasFound, NumberOfIterations, gsSolutionNode = BFS_PopulateGameSpaceTreeOnDemand()
    print(f"The tree contains the solution? {SolutionWasFound}. It took {NumberOfIterations} iterations to discover using BFS.")
    PrintBFSolution(SolutionWasFound, gsSolutionNode)
########################

############################## DFS Code ##############################

# Explore and create game space tree on-demand while traversing in DFS fashion
# Based on DFS solution steps explained in CSC 575 Lecture 7 PPT document (slides 39-61):"
#   1. Pick a starting node [the root] and build a stack of nodes to visit
#   2. Add the node to the stack and mark it as "visited"
#   3. Pick any connected node that is "unvisited" and "unprocessed"
#   4. Mark selected node as "visited" and add it to the stack
#   5. Repeat steps 3 & 4 until no further nodes are connected
#   6. Pop node off the stack and mark it as "processed" and add it to "processed" list
#   7. Use the node from the top of the stack and repeat steps 3 to 6
#   8. When stack is empty push a new "unvisited" and "unprocessed" node to the stack
#   9. Loop through steps 3 to 8 until the solution has been found or there are no more "unvisited" and "unprocessed" nodes
def DFS_PopulateGameSpaceTreeOnDemand():
    global mStartState
    global dictMoveTypes
    dfsVisitedStack = []
    dfsProcessedList = []

    # not initially used but still returned for now.
    solutionFound = False
    iterations = 0
    gsSolutionNode = None

    ##### Move 0 = Root: needed for gsMoveOne's parent
    gsMoveZero = GameSpaceNode("4:4", "StartState", 1, mStartState)
    # 1. Pick a starting node [the root] and build a stack of nodes to visit
    # 2. Add the node to the stack and mark it as "visited"
    gsMoveZero.visited = True
    dfsVisitedStack.append(gsMoveZero)

    ##### Move 1 = Singular Left Leaf
    # Insert first and only left node into Game Space Tree
    # Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
    stateChanged, movedFromTo, mNextState = AttemptStateChange(mStartState, "Diagonal_Down_Left")
    gsMoveOne = GameSpaceNode(movedFromTo, "Diagonal_Down_Left", 2, mNextState)
#    gsMoveOne.gsParent = gsMoveZero
    # 3. Pick any connected node that is "unvisited" and "unprocessed"
    # 4. Mark selected node as "visited" and add it to the stack
    gsMoveOne.visited = True
    dfsVisitedStack.append(gsMoveOne)

    # 5. Repeat steps 3 & 4 until no further nodes are connected
    # randomize the oder in which moves are attempted
    randomMoves = [0,1,2,3,4,5]
    shuffle(randomMoves)
    for i in range(0, 6):
        stateChanged, movedFromTo, mNextState = AttemptStateChange(gsMoveOne.state, dictMoveTypes[randomMoves[i]])
        if stateChanged:
            iterations = iterations + 1
#            print(f"1 iterations({iterations}) | dfsVisitedStack({str(len(dfsVisitedStack))}) | dfsProcessedList({str(len(dfsProcessedList))})")
        
            score = GetScore(mNextState)

            gsNewNode = GameSpaceNode(movedFromTo, dictMoveTypes[randomMoves[i]], score, mNextState)
#               gsNewNode.gsParent = gsDequeued
            # 3. Pick any connected node that is "unvisited" and "unprocessed"
            # 4. Mark selected node as "visited" and add it to the stack
            gsNewNode.visited = True
            dfsVisitedStack.append(gsNewNode)

            if IsSolved(mNextState):
                solutionFound = True
                gsSolutionNode = dfsVisitedStack.pop()
                gsSolutionNode.solution = True
                # 6. Pop node off the stack and mark it as "processed" and add it to "processed" list
                gsSolutionNode.processed = True
                dfsProcessedList.append(gsSolutionNode)
                print("Solved:")
                PrintState(mNextState)
                print("--------------\n")
                return solutionFound, iterations, dfsProcessedList
            else:
                print(f"#{iterations} Call Recurse:")
                DFS_PopulateGameSpaceTreeOnDemand_RecurseDepth(dfsVisitedStack, dfsProcessedList)
        # 5. Repeat steps 3 & 4 until no further nodes are connected
        # 6. Pop node off the stack and mark it as "processed" and add it to "processed" list
        # 7. Use the node from the top of the stack and repeat steps 3 to 6
        #gsPoppedNode = dfsVisitedStack.pop()
        #dfsProcessedList.append(gsPoppedNode)

    print(f"Post Recursive: iterations({iterations}) | dfsVisitedStack({str(len(dfsVisitedStack))}) | dfsProcessedList({str(len(dfsProcessedList))})")
    return solutionFound, iterations, dfsProcessedList

# Recursive helper function of DFS_PopulateGameSpaceTreeOnDemand() above
def DFS_PopulateGameSpaceTreeOnDemand_RecurseDepth(dfsVisitedStack, dfsProcessedList):
    global dictMoveTypes
    global dfsFirstSolutionFound
    global dftTotalSolutionsFound
    solutionFound = False
    gsSolutionNode = None
    gsNewNode = None

#    print(f"Recurse: dfsVisitedStack({str(len(dfsVisitedStack))}) | dfsProcessedList({str(len(dfsProcessedList))})")

    # always start by looking at the top of the stack
    gsStackTopNode = dfsVisitedStack.pop()
    if gsStackTopNode.solution:
        return solutionFound, dfsVisitedStack, dfsProcessedList
    elif not gsStackTopNode.processed:
        # put the node back in the stack because it was only popped to use below
        dfsVisitedStack.append(gsStackTopNode)
    else:
        print(f"Warning: node at the top of the stack already processed {gsStackTopNode}")

    # randomize the oder in which moves are attempted
    randomMoves = [0,1,2,3,4,5]
    shuffle(randomMoves)
    for i in range(0, 6):
        stateChanged, movedFromTo, mNextState = AttemptStateChange(gsStackTopNode.state, dictMoveTypes[randomMoves[i]])
        if stateChanged:
#            iterations = iterations + 1
#            print(f"iterations({iterations}) | dfsVisitedStack({str(len(dfsVisitedStack))}) | dfsProcessedList({str(len(dfsProcessedList))})")
        
            score = GetScore(mNextState)

            gsNewNode = GameSpaceNode(movedFromTo, dictMoveTypes[randomMoves[i]], score, mNextState)
#               gsNewNode.gsParent = gsDequeued
            # 3. Pick any connected node that is "unvisited" and "unprocessed"
            # 4. Mark selected node as "visited" and add it to the stack
            gsNewNode.visited = True
            dfsVisitedStack.append(gsNewNode)

            if IsSolved(mNextState):
                dftTotalSolutionsFound = dftTotalSolutionsFound + 1
                if dftTotalSolutionsFound == 1:
                    dfsFirstSolutionFound = dfsVisitedStack
                solutionFound = True
                gsSolutionNode = dfsVisitedStack.pop()
                gsSolutionNode.solution = True
                # 6. Pop node off the stack and mark it as "processed" and add it to "processed" list
                gsSolutionNode.processed = True
                dfsProcessedList.append(gsSolutionNode)
                print(f"Recurse: dfsVisitedStack({str(len(dfsVisitedStack))}) | dfsProcessedList({str(len(dfsProcessedList))})")
                print("Solved During Recurse:")
                PrintState(mNextState)
                print("--------------\n")
                return solutionFound, dfsVisitedStack, dfsProcessedList
            else:
                DFS_PopulateGameSpaceTreeOnDemand_RecurseDepth(dfsVisitedStack, dfsProcessedList)
        # else:
        #     print(f"State unchanges for node{gsStackTopNode.move}")

    # 5. Repeat steps 3 & 4 until no further nodes are connected
    # 6. Pop node off the stack and mark it as "processed" and add it to "processed" list
    # 7. Use the node from the top of the stack and repeat steps 3 to 6
    if len(dfsVisitedStack) > 0:
        gsPoppedNode = dfsVisitedStack.pop()
        dfsProcessedList.append(gsPoppedNode)
#        DFS_PopulateGameSpaceTreeOnDemand_RecurseDepth(dfsVisitedStack, dfsProcessedList)
    else:
        print(f"Warning: stack is empty")
    return solutionFound, dfsVisitedStack, dfsProcessedList

########################
### DFS driving code ###
# Note: Only DFS or BFS can be run at a time
if versionToRun == "DFS":
    print("----- BFS Output -----")
    dfsFirstSolutionFound = None
    dftTotalSolutionsFound = 0
    SolutionWasFound, NumberOfIterations, dfsProcessedList = DFS_PopulateGameSpaceTreeOnDemand()
    #print(f"The tree contains the solution? {SolutionWasFound}. It took {NumberOfIterations} iterations to discover using BFS.")

    print("----- First BFS Solution -----")
    for i in range(0, len(dfsFirstSolutionFound)):
        PrintState(dfsFirstSolutionFound[i].state)
        print(f"{dfsFirstSolutionFound[i].move} #{i}")

