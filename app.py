from flask import Flask, request, render_template, redirect, url_for, flash
from client import build_image, interact

app = Flask(__name__)
app.secret_key = b'asdfasdf;ljnasdfl;k'

@app.route('/submit', methods=['GET', 'POST'])
def index():
    print(request.form)
    if request.method == 'POST' :
        if 'code' not in request.files:
            return 'No file part'

        language = request.form['language']
        if language not in ['python', 'cpp']:
            return 'Invalid language'

        file = request.files['code']
        if file.filename == '':
            return 'No selected file'
        
        if file:
            # Build image from code
            image = build_image(language, file)

            # Run image
            interact(image, image)

            # # Remove image
            # client.images.remove(image.id, force=True)

            return 'File uploaded successfully'
        return 'Error in upload'
    else:
        return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)

