from flask import Flask, render_template, request, redirect, url_for
import os
from analysis import analyze_emotions

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(url_for('index'))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    scores = analyze_emotions(filepath)
    os.remove(filepath)
    passed = all(score > 5 for score in scores.values()) if scores else False

    return render_template('result.html', scores=scores, passed=passed)


if __name__ == '__main__':
    app.run(debug=True)
