import os
import posixpath

from cognitive_face import CognitiveFaceException
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename

from viz_ai_image.logic import detect_faces_and_emotion, find_max_feeling, clean_data

BASEDIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(posixpath.join(BASEDIR, os.pardir))
UPLOAD_FOLDER = f'{PROJECT_ROOT}/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.route('/', methods=['GET'])
def home():
    return redirect('/upload')


@app.route('/upload', methods=['GET'])
def upload_image():
    return render_template('image_upload.html')


@app.route('/face', methods=['POST'])
def analyze_image():
    # If user submit without file
    if 'file' not in request.files:
        return jsonify(dict(err_msg='No file part'))

    file = request.files['file']
    # if user submit file  without filename
    if file.filename == '':
        return jsonify(dict(err_msg='No selected file'))

    filename = secure_filename(file.filename)
    absolute_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    relative_file_path = url_for('uploaded_file', filename=filename)
    file.save(absolute_file_path)

    try:
        result = detect_faces_and_emotion(absolute_file_path)
    except CognitiveFaceException as e:
        return jsonify(dict(err_msg=e.msg))

    if result:
        # Send only the data for the first face
        result = result[0]

        find_max_feeling(result)
        clean_data(result)

        return jsonify(dict(result=result, filename=relative_file_path))
    else:
        return jsonify(dict(filename=relative_file_path, err_msg='No faces were found'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
