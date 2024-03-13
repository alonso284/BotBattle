"""
ca = (a_output, a_input)
cb = (b_output, b_input)
"""

import os
import queue

def judge(ca, cb, name1='A', name2='B', fobj=None):
    print("starting judge", file=fobj)
    os.write(ca[1], b"0\n")

    player_turn = name1
    while True:
        queue_to_read = ca[0] if player_turn == name1 else cb[0]

        while queue_to_read.empty():
            pass

        next_move = queue_to_read.get()

        # print to fobj the move with the name of the player
        # print("writing to " + name1 if player_turn == 'a' else name2, file=fobj)
        os.write(cb[1] if player_turn == name1 else ca[1], next_move)

        if next_move == b"10\n":
            print("Player " + name1 if player_turn == name1 else name2 + " wins", file=fobj)
            # write EOF to both players
            break

        player_turn = name2 if player_turn == name1 else name1

    print("end of game", file=fobj)


