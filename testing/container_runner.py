import docker
import re
import time
import threading
import string

# this code snippet thakes in a docker image and runs two containters with their intput and output connected to each other

# Constants
DOCKER_IMAGE = "2a9c94ba4afe0be0f43beacc95cd8682ab25290bced66fe524c6e15c133e6653"  # Replace with your actual Docker image name
TIMEOUT = 30  # Timeout in seconds

# Docker client
client = docker.from_env()

# Function to run container and process input/output
def run_container(container, input_queue, output_queue, stop_event):
    try:
        container.start()
        input_stream = container.attach_socket(params={'stdin': 1, 'stream': 1})
        output_stream = container.attach_socket(params={'stdout': 1, 'stream': 1, "logs": 1})
        
        def read_output():
            buffer = ""
            while not stop_event.is_set():
                chunk = output_stream._sock.recv(4096)
                if not chunk:
                    continue
                buffer += chunk.decode('utf-8')
                while re.search(r'\s+', buffer):
                    token, buffer = re.split(r'\s+', buffer, 1)
                    # erase any character that is not a visible character
                    token = ''.join(filter(lambda x: x in string.printable, token))
                    if(token == ""):
                        continue
                    print(f'Container output: {repr(token)} {len(token)}')


                    # TOKEN VALIDATION GOES HERE
                    output_queue.append(token)
                    if token == "FAIL":
                        stop_event.set()
                        return
        
        threading.Thread(target=read_output).start()
        
        while not stop_event.is_set():
            if input_queue:
                next_input = input_queue.pop(0)
                input_stream._sock.send(next_input.encode('utf-8'))
                print(f'Container input: {repr(next_input)} {len(next_input)}')
                input_stream._sock.send(b'\n')
    finally:
        print("Stopping container")
        container.stop()
        container.remove()

# Create containers
container1 = client.containers.create(DOCKER_IMAGE, tty=False, stdin_open=True)
container2 = client.containers.create(DOCKER_IMAGE, tty=False, stdin_open=True)

print(f"Container 1 {container1.name} status: {container1.status}")
print(f"Container 2 {container2.name} status: {container2.status}")


# Input and output queues
input_queue1 = ["pong"]
output_queue1 = []
input_queue2 = []
output_queue2 = []

# Event to signal when to stop
stop_event = threading.Event()

# Start container threads
thread1 = threading.Thread(target=run_container, args=(container1, input_queue1, output_queue1, stop_event))
thread2 = threading.Thread(target=run_container, args=(container2, input_queue2, output_queue2, stop_event))

thread1.start()
thread2.start()

# Main loop to handle communication between containers
start_time = time.time()
try:
    while time.time() - start_time < TIMEOUT and not stop_event.is_set():
        # Process outputs from container1 and send to container2
        while output_queue1:
            token = output_queue1.pop(0)
            # print(f"Container 1 output: {token}")
            input_queue2.append(token)
            if token == "FAIL":
                stop_event.set()
        
        # Process outputs from container2 and send to container1
        while output_queue2:
            token = output_queue2.pop(0)
            # print(f"Container 2 output: {token}")
            input_queue1.append(token)
            if token == "FAIL":
                stop_event.set()
        
        # time.sleep(1)

finally:
    # Cleanup
    stop_event.set()
    thread1.join()
    thread2.join()
