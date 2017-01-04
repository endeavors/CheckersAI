##Checkers against AI/Human

Game is played on the terminal by specifying the indexes of the pieces you want to move. The game is built on a non-bidirectional hierarchy model where the lower levels deal with core game logic and higher levels interact with the user and send commands to the lower levels. This means that most of the input valid is performed at the higher levels. 

* Highest Level to lowest level:
	1. main.py -> Runs the actual game and asks for player's names
	2. checkers.py -> Validates all of the input that is inputted to board logic and plays the game
	3. board.py -> Implements core game logic (ex: Force-jumping as much as possible, checking who won/draw,
			captures pieces, returns the entire updatd board as a string to be printed to the terminal)
	4. piece.py -> Each piece (black/red) on the board is an instance of this Piece class. 
	5. util.py -> Handles enumerations and unicode characters for printing of board/pieces.

#####NOTE: Must be run with Python 3

```Python
>>> Python3 main.py
```

* Moves are defined by the following syntax: '50 41' 
	* where 5 and 0 are the row and column indices, respectively, of the piece you want to move and 4 and 1 are the row and column indices to where you want the piece to be moved.

* All jumps are forced until no jumps are available.
* In the case of multiple jump paths being available to the **SAME** end position, the user is shown and asked which jump path to take. 

###Start of Game:

[![Screen Shot 2017-01-04 at 6.53.23 AM.png](https://s29.postimg.org/3y3uksdnb/Screen_Shot_2017_01_04_at_6_53_23_AM.png)](https://postimg.org/image/e869k13ir/)


###After First Move:

[![Screen Shot 2017-01-04 at 6.53.49 AM.png](https://s23.postimg.org/nvo3nnx4b/Screen_Shot_2017_01_04_at_6_53_49_AM.png)](https://postimg.org/image/aer54smsn/)

###Things not done yet:
* No kings are crowned currently. This means when a piece gets to the end of the row = 0 or row = 7, it doesn't have the ability to move backwards as of now.
* AI is not added yet. You can only play with another human currently.

###Plans for AI:
* Alpha-Beta Pruning with Iterative Deepening. Please don't do Depth-first search or Breadth First Search on this. You will be wasting resources. 
* Don't create all the children at once for each board node, otherwise there is no point of doing Alpha-Beta Pruning and Minimax wouls suffice. 
