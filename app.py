import os
from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, session
import pandas as pd
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['csv'])


app = Flask(__name__)
# Setting secret key for flask session
app.secret_key = b'unlock'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Checking if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def upload(filename=None):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #creating session of filename
            if filename:
                session["filename"] = filename

    return render_template('index.html', filename=filename)

@app.route('/graph/', methods=['GET', 'POST'])
def graph(xaxis=None, yaxis=None, data=None, column=None):
    if request.method == 'POST':
        xaxis = request.form['x_data']
        yaxis = request.form['y_data']

    filename = session.get('filename', None)

    if filename:
        df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        column = list(df)
        data = [list(df[d]) for d in column]

    return render_template('graph.html', xaxis=xaxis, yaxis=yaxis, column=column, data=data)


if __name__ == "__main__":
    app.run(debug = True)
