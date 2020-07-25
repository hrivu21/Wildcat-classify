# Importing necessary packages
# import numpy as np
from flask import Flask, request, render_template, flash, redirect, url_for
# import pickle
from fastai import *
from fastai.vision import *
import os
from werkzeug.utils import secure_filename

# uploads_dir = os.path.join(app.instance_path, 'images')
UPLOAD_FOLDER = '\\images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

cwd = os.getcwd()
path = cwd + '/model'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "5da5ea90223c3d8d5843"

model = load_learner(path, 'model.pkl')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            f_name = secure_filename(file.filename)
            file.save(f_name)
            path = Path(cwd + '/' + f_name)
            img = open_image(path)
            prediction, _, _ = model.predict(img)
            flash(f'The predicted class is: {str(prediction).capitalize()}', 'success')
            try:
                os.remove(f'{cwd}/{f_name}')
            except:
                pass
            return render_template('index.html', f_name=f_name)

        flash('The extension should be .jpg', 'warning')
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
