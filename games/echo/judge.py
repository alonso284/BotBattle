"""
# Send input to the container
socket_1._sock.send(b'0\n')

# Read from container1 (example, adjust buffer size as needed)
out1 = socket_1._sock.recv(1024)
out1_str = out1.decode('utf-8')
print(out1_str)
"""

import os
import queue
import docker

def judge(socket_1, socket_2):
    socket_1._sock.send(b'Hello world\n')

    turn = True
    c = 5

    while c > 0:
        socket_in  = socket_1 if turn else socket_2
        socket_out = socket_2 if turn else socket_1

        out = socket_in._sock.recv(1024)
        socket_out._sock.send(out)

        turn = not turn

        c -= 1


