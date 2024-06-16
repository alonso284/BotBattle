
import random
import time
moves = ["ping", "pong", "FAIL"]

random.seed(time.time())

while True:
    move = input()

    next = random.choice(moves)

    if move == "pong":
        print(next, flush=True)
    if move == "ping":
        print(next, flush=True)
    elif move == "FAIL":
        break
    else:
        print(f"error: move", flush=True)
        break

    if next == "FAIL":
        break