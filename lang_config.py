LANGUAGES = {
# PYTHON
    'python': {
        'display_name': 'Python',
        'dockerfile': 
"""
FROM python:3.9-slim
WORKDIR /usr/src/app
COPY . .
CMD [ "python", "./app.py" ]
""",
        'extension': '.py'
    },

# C++
    'cpp': {
        'display_name': 'C++',
        'dockerfile': 
"""
FROM gcc:10.2
WORKDIR /usr/src/app
COPY . .
RUN g++ -o app app.cpp
CMD [ "./app" ]
""",
        'extension': '.cpp'
    },

# JAVA
    'java': {
        'display_name': 'Java',
        'dockerfile':
"""
FROM openjdk:11
WORKDIR /usr/src/app
COPY . .
RUN javac app.java
CMD [ "java", "app" ]
""",
        'extension': '.java'
    }
}