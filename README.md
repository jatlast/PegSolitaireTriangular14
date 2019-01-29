# PegSolitaireTriangular14

PegSolitaireTriangular14 is the result of the following homework assignment.

```
Master's Degree: University of Michigan - Computer Science & Information Systems
Course: CSC 546 - Advanced Artificial Intelligence

Assignment Homework 2: Due: 01/29/2019 5:59 PM | Began Coding: 01/25/2019 11:20 PM
(2.0) Programming:
    (ii) For graduate students find a puzzle (the triangular marble solitaire game 
        with 14 marbles is a fun one) or other problem of interest and code it up. 
        Use either the BFS or the DFS to do this.
            (a) Extra Credit (5 points) – Also write a breadth-first search or 
                explain thru complexity analysis of space and memory requirements due 
                to depth and branching factor why it would not work on that problem.
```

## False Starts

1) Tried to create the entire game state tree as a matrix without keeping matrix dimentionality consistant.
2) Tried to do BFS on the inconstant matrix.
3) Tried to create a graph of the game state tree using a Python dictionary to represent nodes as keys and edges as lists.

## Final Solution(s)

1) Adding a "parent" variable to the GameStateNode class allowed for recreating the moves
from the solution state back to the start state once the solution node had been found.

## Chosen Technologies

Motivation: Become more familiar with the following.
1) Developing with Python 3.7 in Windows environment
2) IDE - Visual Studio Code
3) GitHub (a very powerful tool ignored for too long)

## The following websites were referenced

* [Wikipedia's Peg_solitaire](https://en.wikipedia.org/wiki/Peg_solitaire) - For understanding the game
* [How to Implement Breadth-First-Search in Python](https://pythoninwonderland.wordpress.com/2017/03/18/how-to-implement-breadth-first-search-in-python/) - The 8 BFS steps proved most useful

### Prerequisites

- Python 3.6+

### Installing
```
Just get the "PegSolitaireTriangular14" project.
It should run in any Python 3.6+ environment
```

## License

This project is not licensed but feel free to play with any part you so desire.

## Acknowledgments

* wikipedia
* pythoninwonderland.wordpress.com
* Google's vast doorway to every tid-bit of documentation on the internet
* All those wonderfully generous documentation writers and question answerers
