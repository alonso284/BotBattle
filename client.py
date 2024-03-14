import docker
import tempfile
import os
# import threading
import concurrent.futures

from games.echo.judge import judge
from lang_config import LANGUAGES

client = docker.from_env()

def build_image(language, code):
    if language not in LANGUAGES:
        raise ValueError("Invalid language")
    dockerfile_content = LANGUAGES[language]['dockerfile']
    image_tag = language + "_image"
    file_name = "app" + LANGUAGES[language]['extension']

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


def battle(image1, image2) -> bool:
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
    res = judge(socket_1, socket_2)

    # Close socket
    socket_1.close()
    socket_2.close()

    # # Cleanup
    # container1.stop()
    # container2.stop()

    # Use a non-blocking stop by specifying timeout=0
    container1.stop(timeout=0)
    container2.stop(timeout=0)

    # Forcefully remove the container, which stops it if it's running
    container1.remove(force=True)
    container2.remove(force=True)


    # remove the container
    # container1.remove(force=True)
    print("Battle finished")
    return res

def interact(language1, language2, code1, code2) -> bool:
    runs = 3
    socket_1_wins = 0

    # Build images from code
    image1 = build_image(language1, code1)
    image2 = build_image(language2, code2)

    # Use ThreadPoolExecutor to run battle function in threads and capture return values
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the battle function to an iterable of arguments, in this case, multiple calls with the same args
        future_to_battle = {executor.submit(battle, image1.id, image2.id): i for i in range(runs)}
        
        for future in concurrent.futures.as_completed(future_to_battle):
            result = future.result()
            print("Battle finished")
            print(result)
            # Process result here (example: increment socket_1_wins based on result)
            if result:  # Assuming battle function returns a string indicating the winner
                socket_1_wins += 1

    # Do something with socket_1_wins or other results here
    print("All battles finished")
    print("Socket 1 wins:", socket_1_wins)
    print("Socket 2 wins:", runs - socket_1_wins)

    return socket_1_wins > runs // 2

