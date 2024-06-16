from flask import Flask, request, render_template, redirect, url_for, flash
from client import build_image, interact
from lang_config import LANGUAGES

app = Flask(__name__)
app.secret_key = b'asdfasdf;ljnasdfl;k'

@app.route('/submit', methods=['GET', 'POST'])
def index():
    print(request.form)
    if request.method == 'POST' :
        if 'code1' not in request.files or 'code2' not in request.files:
            return 'No file part'

        language1 = request.form['language1']
        if language1 not in LANGUAGES:
            return 'Invalid language'
        
        language2 = request.form['language2']
        if language2 not in LANGUAGES:
            return 'Invalid language'

        file1 = request.files['code1']
        if file1.filename == '':
            return 'No selected file'
        
        file2 = request.files['code2']
        if file2.filename == '':
            return 'No selected file'
        
        if file1 and file2:

            # Run image
            res = interact(language1, language2, file1, file2)

            # # Remove image
            # client.images.remove(image.id, force=True)

            # return 'File uploaded successfully'
            return "Winner: " + ("A" if res else "B")
        return 'Error in upload'
    else:
        return render_template('submit.html', languages=LANGUAGES)

if __name__ == '__main__':
    app.run(debug=True)

