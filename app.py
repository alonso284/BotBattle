from flask import Flask, request, render_template, redirect, url_for, flash
 
# use later for temporary access to files, for now, store in /temp
import tempfile

from client import build_language_image
from croupier_judge import interact

app = Flask(__name__)
app.secret_key = b'asdfasdf;ljnasdfl;k'

@app.route('/submit', methods=['GET', 'POST'])
def index():
    print(request.form)
    if request.method == 'POST':
        if 'code' not in request.files:
            return 'No file part'
        file = request.files['code']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Process the file content here
            # content = file.read()  # Read the file's content

            # print(content.decode('utf-8'))
            
            # Optionally, save the file to the server
            file.save('./temp/app.py')

            image_id = build_language_image('python')

            interact(f"docker run -i {image_id}", f"docker run -i {image_id}")
            
            return 'File uploaded successfully'
        return 'Error in upload'
    else:
        return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)

