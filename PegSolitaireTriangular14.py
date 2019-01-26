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

# Try to find a zero node that can be shifted according to the specified changeState
#   Note: Calling function must determine if game state was changed.
def AttemptStateChange(mCurrentState, changeType):
    changedState = False
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
                    changedState = True
                    return changedState, mCurrentState
    # No change to game state
    return changedState, mCurrentState

PrintState(mStartState)

stateChanged, mCurrentState = AttemptStateChange(mStartState, "Diagonal_Down_Left")

print(f"The game state has changed: {stateChanged}")

PrintState(mCurrentState)

stateChanged, mCurrentState = AttemptStateChange(mCurrentState, "Right")

print(f"The game state has changed: {stateChanged}")

PrintState(mCurrentState)

stateChanged, mCurrentState = AttemptStateChange(mCurrentState, "Diagonal_Up_Right")

print(f"The game state has changed: {stateChanged}")

PrintState(mCurrentState)

stateChanged, mCurrentState = AttemptStateChange(mCurrentState, "Diagonal_Up_Left")

print(f"The game state has changed: {stateChanged}")

PrintState(mCurrentState)

stateChanged, mCurrentState = AttemptStateChange(mCurrentState, "Left")

print(f"The game state has changed: {stateChanged}")

PrintState(mCurrentState)

stateChanged, mCurrentState = AttemptStateChange(mCurrentState, "Right")

print(f"The game state has changed: {stateChanged}")

PrintState(mCurrentState)

print(f"The problem solved? {IsSolved(mCurrentState)}")


