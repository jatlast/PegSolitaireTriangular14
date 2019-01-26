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
    if sum == 13:
        print(f"Warning: Score{sum} should never happen because it is the solution.")
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
  
    print(f"Attempt {changeType} state change")
    for x in range(0, 9):
        for y in range(0, 9):
            if mCurrentState[x][y] == 0:
                if ((x + xDif + xDif) < 9) and ((y + yDif + yDif) < 9) and mCurrentState[x+xDif][y+yDif] == 1 and mCurrentState[x+xDif+xDif][y+yDif+yDif] == 1:
                    print(f"x{x},y{y} and {mCurrentState[x+xDif][y+yDif]} and {mCurrentState[x+xDif+xDif][y+yDif+yDif]}")
                    mCurrentState[x][y] = 1
                    mCurrentState[x+xDif][y+yDif] = 0
                    mCurrentState[x+xDif+xDif][y+yDif+yDif] = 0
                    pegMoveFromTo = str(x+xDif+xDif) + ":" + str(y+yDif+yDif) + "-" + str(x) + ":" + str(y)
                    changedState = True
                    return changedState, pegMoveFromTo, mCurrentState
    # No change to game state
    return changedState, pegMoveFromTo, mCurrentState

# Adapted from:
# Python program to demonstrate insert operation in binary search tree  
# https://www.geeksforgeeks.org/binary-search-tree-set-1-search-and-insertion/
  
# A utility class that represents an individual node in six-leaf tree
class GameSpaceNode: 
    def __init__(self, sMove, sMoveType, nSore, mState):
        self.one = None
        self.two = None
        self.three = None
        self.four = None
        self.five = None
        self.six = None
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

# A utility function to insert a new node with the given state into the Game Space Tree
def InsertNodeIntoGameSpaceTree(root, node):
    if root is None:
        root = node
    else:
        # add to current root level leaves
        if root.score == node.score:
            if root.one is None:
                root.one = node
            elif root.two is None:
                root.two = node
            elif root.three is None:
                root.three = node
            elif root.four is None:
                root.four = node
            elif root.five is None:
                root.five = node
            elif root.six is None:
                root.six = node
            else:
                print(f"Warning 1: this should never happen")
        # insert another level to the tree and populate leaves with recursive call
        elif root.score < node.score:
            if root.one is not None:
                InsertNodeIntoGameSpaceTree(root.one, node)
            elif root.two is not None:
                InsertNodeIntoGameSpaceTree(root.two, node)
            elif root.three is not None:
                InsertNodeIntoGameSpaceTree(root.three, node)
            elif root.four is not None:
                InsertNodeIntoGameSpaceTree(root.four, node)
            elif root.five is not None:
                InsertNodeIntoGameSpaceTree(root.five, node)
            elif root.six is not None:
                InsertNodeIntoGameSpaceTree(root.six, node)
            else:
                print(f"Warning 2: this should never happen")
        else:
            print(f"Warning 3: this should never happen")

# A utility function to do inorder tree traversal
def inorder(root):
    if root:
        inorder(root.one)
        inorder(root.two)
        inorder(root.three)
        inorder(root.four)
        inorder(root.five)
        inorder(root.six)
        print(root)
        PrintState(root.state)

def PopulateOneLevelOfGameSpaceTree(currentRootNode, mCurrentState):

    dictMoveTypes = {
          0 : "Diagonal_Down_Left"
        , 1 : "Diagonal_Down_Right"
        , 2 : "Diagonal_Up_Left"
        , 3 : "Diagonal_Up_Right"
        , 4 : "Left"
        , 5 : "Right"
    }

    # randomize the oder in which moves are attempted
    randomMoves = [0,1,2,3,4,5]
    shuffle(randomMoves)
    for i in range(0, 6):
        stateChanged, movedFromTo, mNextState = AttemptStateChange(mCurrentState, dictMoveTypes[randomMoves[i]])
        if stateChanged:
            score = GetScore(mNextState)
            nextMoveNode = GameSpaceNode(movedFromTo, dictMoveTypes[randomMoves[i]], score, mNextState)
            InsertNodeIntoGameSpaceTree(currentRootNode, nextMoveNode)
        else:
            print(f"Unable to move {randomMoves[i]} = {dictMoveTypes[randomMoves[i]]}")


##### Move 0 = Root
# Insert root node into Game Space Tree
# Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
rootNode = GameSpaceNode("Initial", "Static", 1, mStartState)

##### Move 1 = Singular Left Leaf
# Insert first and only left node into Game Space Tree
# Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
stateChanged, movedFromTo, mCurrentState = AttemptStateChange(mStartState, "Diagonal_Down_Left")
firstMoveNode = GameSpaceNode(movedFromTo, "Diagonal_Down_Left", 2, mCurrentState)
InsertNodeIntoGameSpaceTree(rootNode.one, firstMoveNode)

inorder(rootNode)

print(f"Current Game Score: {GetScore(mCurrentState)}")

print(f"The problem solved? {IsSolved(mCurrentState)}")


