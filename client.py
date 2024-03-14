import docker
import tempfile
import os
import threading

from games.echo.judge import judge

client = docker.from_env()

def build_image(language, code):
    if language == 'python':
        # Define the content of the temporary Dockerfile
        dockerfile_content = """
FROM python:3.9-slim
WORKDIR /usr/src/app
COPY . .
CMD [ "python", "./app.py" ]
        """
        extension = ".py"

    elif language == 'cpp':
        # Define the content of the temporary Dockerfile
        dockerfile_content = """
FROM gcc:10.2
WORKDIR /usr/src/app
COPY . .
RUN g++ -o app app.cpp
CMD [ "./app" ]
        """
        extension = ".cpp"
    else:
        raise ValueError("Unsupported language")
    
    image_tag = "language_" + language + "_image"
    file_name = "app" + extension

    # Create a temporary directory to store the Dockerfile and code file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define the path to the temporary Dockerfile
        dockerfile_path = os.path.join(temp_dir, 'Dockerfile')

        # Write the Dockerfile content to the temporary file
        with open(dockerfile_path, 'w') as dockerfile:
            dockerfile.write(dockerfile_content)

        # Define the path to the temporary code file
        code_file_path = os.path.join(temp_dir, file_name)

        # Write the code content to the temporary file
        with open(code_file_path, 'wb') as code_file:
            code_file.write(code.read())

        # Build the Docker image from the temporary Dockerfile
        image, _ = client.images.build(path=temp_dir, tag=image_tag)

        print("Image built successfully")
        print("Image ID:", image.id)
        return image


def battle(image1, image2):
    # Run image from build_image
    container1 = client.containers.run(image1, detach=True, stdin_open=True, tty=False)
    container2 = client.containers.run(image2, detach=True, stdin_open=True, tty=False)

    # Attach to the container's stdin, stdout, and stderr
    print("Creating Sockets")
    socket_1 = container1.attach_socket(params={'stdout': 1, 'stdin': 1,'stream': 1})
    socket_2 = container2.attach_socket(params={'stdout': 1, 'stdin': 1,'stream': 1})

    # Set the sockets to non-blocking mode (optional, depending on your use case)
    print("Setting Sockets")
    socket_1._sock.setblocking(True)
    socket_2._sock.setblocking(True)

    # TODO START THE GAME
    judge(socket_1, socket_2)

    # Close socket
    socket_1.close()
    socket_2.close()

    # Cleanup
    container1.stop()
    container2.stop()

    # remove the container
    # container1.remove(force=True)

    print("Battle finished")

    

def interact(image1, image2):

    threads = []
    # Run battle many times in threads
    for i in range(10):
        t = threading.Thread(target=battle, args=(image1.id, image2.id))
        threads.append(t)
        t.start()


    for t in threads:
        t.join()

    print("All battles finished")



