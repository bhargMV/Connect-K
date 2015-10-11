# AI-Homework2
This assignment involves implementation of the minimax and alpha-beta (with pruning) adversarial game
search techniques.

Submitted by:
Atanu Ghosh (110280569), Bhargava Mourya Venishetty (110308227)
Atanu Ghosh <atghosh@cs.stonybrook.edu>, Bhargava Mourya Venishetty <bvenishetty@cs.stonybrook.edu>

(Question 1
Minimax algorithm:

References:

1) https://en.wikipedia.org/wiki/Minimax
2) CSE537 Lecture Notes

Player 2 (☻) puts a token in column 1
Win for ☻!

  0 1 2 3 4 5 6
0 ☻   ☻ ☻ ☺
1 ☺   ☺ ☺ ☺
2 ☻   ☻ ☻ ☻
3 ☺   ☺ ☺ ☺
4 ☻ ☻ ☻ ☻ ☺
5 ☻ ☻ ☺ ☺ ☺

Execution Time: 16.517018
Nodes Expanded for Minimax: 29672

The above is the output on running basic_player with new_player (with new evaluate function).
New player wins the game.

(Question 2)
New Evaluation Function:
This function calculates the difference of number of possible wins of 'O' and  number of possible wins of 'X' for the given
game state. In the Minimax implementation, MAX chooses a move such that it has highest chance of win( i.e, The state which has highest
value returned by evaluation function)  and  MIN chooses a move such that MAX has lowest chance of win( i.e, The state which has lowest
value returned by evaluation function).

(Question 3)
Alpha-Beta Search algorithm (with pruning):

Implemented using recursion.

References:
1) https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
2) CSE537 Lecture Notes

Player 1 (☺) puts a token in column 5
Win for ☺!

  0 1 2 3 4 5 6
0     ☻ ☻
1     ☺ ☺
2     ☺ ☻
3     ☻ ☺
4   ☻ ☺ ☻ ☺
5   ☺ ☺ ☻ ☻ ☺

Execution Time: 10.446128
Nodes Expanded for Alpha-Beta: 4689

The above is the output on running alphabeta_player (with new evaluate function) vs basic_player
Aplha Beta player wins the game.

Running the Game

To run the game, just change the players (basic_player, alphabeta_player, random_player, human_player etc)
in lab3.py and then run 'python lab3.py'

(Question 4)

Connect k
Connect-k is also implemented by passing an extra k_value argument in ConnectFourBoard Class.
The default value of this is 4. This value can be overridden by passing a value for k while
creating the ConnectFourBoard object.

(Question 5)
This report and results.
