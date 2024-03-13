import docker
import subprocess

client = docker.from_env()

def build_language_image(language):
    if language == 'python':
        dockerfile = """
FROM python:3.9-slim
WORKDIR /usr/src/app
COPY . .
CMD [ "python", "./app.py" ]
        """
        # Write the Dockerfile to a temporary file
        with open("./temp/Dockerfile", "w") as dockerfile_file:
            dockerfile_file.write(dockerfile)
        
        # Build the Docker image
        image, _ = client.images.build(path="./temp", dockerfile="Dockerfile", tag="language_python_image")
        
        print("Image built successfully")
        print("Image ID:", image.id)
        return image.id
    else:
        raise ValueError("Unsupported language")