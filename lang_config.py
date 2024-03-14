LANGUAGES = {
# PYTHON
    'python': {
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
        'dockerfile': 
"""
FROM gcc:10.2
WORKDIR /usr/src/app
COPY . .
RUN g++ -o app app.cpp
CMD [ "./app" ]
""",
        'extension': '.cpp'
    }
}