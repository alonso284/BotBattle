"""
This is a bot that plays the game of Connect Four

Player may receivce the following inputs:
    - 0: to indicate that the player is the first to move
    - 1-9: to indicate the opponent's move
    - 200: to indicate that the player has won
    - 201: to indicate that the opponent has won
    - 202: to indicate that the game is a draw
    - 400: to indicate that the player's move is invalid

The player may return the following outputs:
    - 1-9: to indicate the player's move

The board is a 9x5 grid, with the left most column being column 1 and the right most column being column 9.
"""

import random
import os

def make_move(opponent_move: int):
    return random.randint(1, 10)

with open('p2.txt', 'w') as f:
    f.write('')

while True:
    opponents_move = int(input())
    if(opponents_move >= 10):
        break
    move = make_move(opponents_move)
    print(move, flush=True)
    # print current working directory
    # print(os.getcwd())
    # append move to a file aclled p1.txt
    with open('p2.txt', 'a') as f:
        f.write(str(opponents_move) + str(move) + '\n')
    f.close()
    if(move == 10):
        break


