import os
import queue
import docker
import random
import socket
import subprocess
import threading
import re

def parser(q: queue.Queue, socket_out: socket.socket):
    print('Starting parser')
    last_token = b''
    while True:
        try:
            print("Fetching data")
            # data = socket_out._sock.recv(1024)  # Directly use recv on the socket object
            if not socket_out._sock:
                print("Socket closed, stopping parser")
                break
            data = socket_out._sock.recv(1024)  # Directly use recv on the socket object
            if not data:
                print("No data, stopping parser")
                break  # Correct way to exit the loop if connection is closed

            print("Data fetched")
            # Tokenize considering spaces, tabs, and newlines

            # tokens = data.replace(b'\t', b' ').replace(b'\n', b' ').split(b' ')
            tokens = data.replace(b'\t', b' ').replace(b'\n', b' ').split(b' ')
            tokens[0] = last_token + tokens[0]
            last_token = tokens.pop()
            for token in tokens:
                q.put(token)

        except socket.error as e:
            print(f"Socket error: {e}")
            break

def judge(socket_1: tuple[socket.socket, socket.socket], 
          socket_2: tuple[socket.socket, socket.socket], 
          starter: bool = False) -> bool:
    
    print('Starting judge')
    q1, q2 = queue.Queue(), queue.Queue()
    s1_out, s2_out = socket_1[1], socket_2[1]
    s1_in, s2_in = socket_1[0], socket_2[0]

    turn = starter
    if turn:
        s1_in._sock.send(b'Hello\n')  # Use send directly on the socket object
    else:
        s2_in._sock.send(b'Hello\n')

    # Create and start threads for parsing
    p1 = threading.Thread(target=parser, args=(q1, s1_out))
    p2 = threading.Thread(target=parser, args=(q2, s2_out))
    p1.start()
    p2.start()

    c = 5

    while c > 0:
        print('Turn: ' + str(turn))
        q = q1 if turn else q2
        socket_in = s2_in if turn else s1_in
        # socket_out = s1_out if turn else s2_out
        # parser(q, socket_out)

        token = q.get()  # This will block until an item is available
        print('Got token: ' + str(token))
        # socket_in._sock.send(token)  # Use send directly
        socket_in._sock.send(token + b'\n')  # Use send directly

        turn = not turn
        c -= 1

    # Ensure threads are given a chance to exit cleanly
    # p1.join()
    # p2.join()

    res = random.choice([True, False])
    print(res)
    return res
