import random
import time
moves = ["ping      ", "pong     ping       ", "FAIL    "]

random.seed(time.time())

while True:
    move = input()

    next = random.choice(moves)

    if move == "pong":
        print(next)
    elif move == "ping":
        print(next)
    elif move == "FAIL":
        break
    else:
        print(f"error:move{move}{len(move)}")
        break

    if next == "FAIL":
        break
