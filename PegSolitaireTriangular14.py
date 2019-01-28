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
######################################################

from random import shuffle # used to randomize the order in which moves are made
import queue # for Breadth-First-Search (BFS)
from collections import defaultdict # for Graph Path to prevent throwing errors for "key not found"

# an individual node representing a specific game state
class GameSpaceNode: 
    def __init__(self, sMove, sMoveType, nSore, mState):
        self.explored = False
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
        return "GameSpaceNode(explored=" + str(self.explored) + ", move=" + self.move + ", moveType=" + self.moveType + ", score=" + str(self.score) + ")"

#####################################################
############### Adapted External Code ###############
# This code is contributed by Kanav Malhotra 
#   https://www.geeksforgeeks.org/graph-and-its-representations/
"""
A Python program to demonstrate the adjacency
list representation of the graph
"""
# A class to represent the adjacency list of the node
class AdjNode:
	def __init__(self, vertexNum):
		self.vertex = vertexNum
		self.next = None

# A class to represent a graph. A graph 
# is the list of the adjacency lists. 
# Size of the array will be the no. of the 
# vertices "V"
class Graph:
	def __init__(self, vertices):
		self.V = vertices
		self.graph = [None] * self.V

	# Function to add an edge in an undirected graph
	def add_edge(self, src, dest):
		# Adding the node to the source node
		node = AdjNode(dest)
		node.next = self.graph[src]
		self.graph[src] = node

		# Adding the source node to the destination as
		# it is the undirected graph
		# node = AdjNode(src)
		# node.next = self.graph[dest]
		# self.graph[dest] = node

	# Function to print the graph
	def print_graph(self):
		for i in range(self.V):
			print("Adjacency list of vertex {}\n head".format(i), end="")
			temp = self.graph[i]
			while temp:
				print(" -> {}".format(temp.vertex), end="")
				temp = temp.next
			print(" \n")

# V = 5
# graph = Graph(V)
# graph.add_edge(0, 1)
# graph.add_edge(0, 4)
# graph.add_edge(1, 2)
# graph.add_edge(1, 3)
# graph.add_edge(1, 4)
# graph.add_edge(2, 3)
# graph.add_edge(3, 4)

# graph.print_graph()
#####################################################

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
                        SolutionFound = True
                        return SolutionFound, iterations
    return SolutionFound, iterations
#               else:
#                   print(f"Unable to move {randomMoves[i]} = {dictMoveTypes[randomMoves[i]]}")

def PopulateGameSpaceTreeAndPaths(GameSpaceTree, dictGameSpacePaths):
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
    GameSpaceTree[0].append(GameSpaceNode("4:4", "Static", 1, mStartState))

#    dictGameSpacePaths["4:4"] = ["root"]

    ##### Move 1 = Singular Left Leaf
    # Insert first and only left node into Game Space Tree
    # Note: because of symmetry, the entire right (or left) half of the state space tree can be ignored
    stateChanged, movedFromTo, mNextState = AttemptStateChange(mStartState, "Diagonal_Down_Left")
    GameSpaceTree.append([]) # add an empty row 1
    GameSpaceTree[1].append(GameSpaceNode(movedFromTo, "Diagonal_Down_Left", 2, mNextState))

    dictGameSpacePaths["4:4"] = [movedFromTo]

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
                    if dictGameSpacePaths[mCurrentMove] is None:
                        dictGameSpacePaths[mCurrentMove] = [movedFromTo]
                    else:
                        dictGameSpacePaths[mCurrentMove] += [movedFromTo]

                    if IsSolved(mNextState):
                        print("Solved:")
                        PrintState(mNextState)
                        SolutionFound = True
                        return SolutionFound, iterations
    return SolutionFound, iterations


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


# 2D matrix where rows are of equal game scores and columns are increasing game scores
GameSpaceTree = []

dictGameSpacePaths = defaultdict(list)

# dictGameSpacePaths['a:b'] = ["a"]
# if dictGameSpacePaths['a:b'] is None:
#     dictGameSpacePaths['a:b'] = ["b"]
# else:
#     dictGameSpacePaths['a:b'] += ["b"]
# print(dictGameSpacePaths['a:b'])

SolutionWasFound, NumberOfIterations = PopulateGameSpaceTreeAndPaths(GameSpaceTree, dictGameSpacePaths)
print(dictGameSpacePaths)

#SolutionWasFound, NumberOfIterations = PopulateGameSpaceTree(GameSpaceTree)
print(f"The tree contains the solution? {SolutionWasFound}. It took {NumberOfIterations} iterations.")

def PrintGameSpaceTree(GameSpaceTree):
    rows = len(GameSpaceTree)
    for r in range(0, rows):
        for c in range(0, len(GameSpaceTree[r])):
#            print(f"[{r}][{c}] = {GameSpaceTree[r][c]}")
            print(f"[{r}][{c}]", end=" ")
        print("\n")

def PrintGameSpaceTreeBranchingFactors(GameSpaceTree):
    totalNodes = 0
    rows = len(GameSpaceTree)
    for r in range(0, rows):
        totalNodes = totalNodes + len(GameSpaceTree[r])
        print(f"Row[{r}]\t has {str(len(GameSpaceTree[r]))} nodes")
    print(f"For a total of {totalNodes} nodes")

PrintGameSpaceTreeBranchingFactors(GameSpaceTree)

# =======================================
# Implement BFS
def Borrowed_BFS(queue=None):
    global GameSpaceTree
    current_index = queue.get()
    print(f"current_index = {current_index}")

    current_x, current_y = current_index[0], current_index[1]

    score = GameSpaceTree[current_y][current_x].score

    if score == 3: return current_x,current_y

    iterations = 0

    while iterations < 10:
        for n in range(current_x-1,current_x+2):
            for m in range(current_y-1,current_y+2):
                print(f"n[{n}]m[{m}]")
                iterations = iterations + 1
                if not (n==current_x and m==current_y) \
                    and n>-1 and m>-1 \
                    and n<len(GameSpaceTree[n]) and m<len(GameSpaceTree[m]) \
                    and (n,m) not in queue.queue :
                        queue.put((n,m))
                else:
                    print(f"else: {iterations}, qSize: {queue.qsize()}")
    return Borrowed_BFS(queue) # currently causes an infinite loop

PrintGameSpaceTree(GameSpaceTree)

# 4. Queue for BFS
#start_queue = queue.Queue()
#start_queue.put((0,0))
#BFS_results = BFS(start_queue)

start_queue = queue.Queue()
start_queue.put((0,0))
#MatrixBFS(start_queue)
#print(f"[{0}][{0}] = {GameSpaceTree[0][0]}")
#print(f"Results of BFS = {BFS_results}")
