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
#   https://en.wikipedia.org/wiki/Peg_solitaire
#   
######################################################

from random import shuffle # used to randomize the order in which moves are made

# Check if the current game state is already solved
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

# Check if the current game state is already solved
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

# Check if the current game state is already solved
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

# an individual node representing a specific game state
class GameSpaceNode: 
    def __init__(self, sMove, sMoveType, nSore, mState):
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
        return "GameSpaceNode(move=" + self.move + ", moveType=" + self.moveType + ", score=" + str(self.score) + ")"

def PopulateGameSpaceTree(GameSpaceTree):
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
    #nodes = len(mStartState)
    #print(f"nodes={nodes}")

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

    SolutionFound = False
    iterations = 0
    for row in range(2, 15):
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
                    GameSpaceTree[score-1].append(GameSpaceNode(movedFromTo, dictMoveTypes[randomMoves[i]], score, mNextState))
                    if IsSolved(mNextState):
                        print("Solved:")
                        PrintState(mNextState)
                        SolutionFound = True
                        return SolutionFound, iterations
    return SolutionFound, iterations
#               else:
#                   print(f"Unable to move {randomMoves[i]} = {dictMoveTypes[randomMoves[i]]}")

# 2D matrix where rows are of equal game scores and columns are increasing game scores
GameSpaceTree = []

SolutionWasFound, NumberOfIterations = PopulateGameSpaceTree(GameSpaceTree)
print(f"The tree contains the solution? {SolutionWasFound}. It took {NumberOfIterations} iterations.")

#PopulateOneLevelOfGameSpaceTree(GameSpaceTree, mCurrentState)

def PrintGameSpaceTree(GameSpaceTree):
    rows = len(GameSpaceTree)
    for r in range(0, rows):
        for c in range(0, len(GameSpaceTree[r])):
            print(f"[{r}][{c}] = {GameSpaceTree[r][c]}")

#PrintGameSpaceTree(GameSpaceTree)

#print(f"Current Game Score: {GetScore(mCurrentState)}")

#print(f"The problem solved? {IsSolved(mCurrentState)}")


