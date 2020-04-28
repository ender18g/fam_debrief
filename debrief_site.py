import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory, render_template
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFilter
from new_graph import create_report


# UPLOAD_FOLDER = '/home/allan18g/give_a_nam/images/'
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('show_report',filename=filename))
    return render_template('upload.html')

@app.route('/index')
def index():
  return render_template('index.html')


@app.route('/uploads/<filename>')
def show_report(filename):
    create_report(app.config['UPLOAD_FOLDER'],filename,166,194)
    return send_from_directory(app.config['UPLOAD_FOLDER']+'pdf/',
                               filename.split('.')[0]+'.pdf')

# @app.route('/show/<filename>')
# def show_image(filename):
#     create_report(filename)
#     filename = url_for('uploaded_file',filename=filename)
#     return render_template('show_image.html', filename=filename)


# def add_nam(filename):
#     im1 = Image.open(app.config['UPLOAD_FOLDER']+filename)
#     im2 = Image.open(app.config['UPLOAD_FOLDER'] + 'nam.png')
#     fraction = (im1.height/im2.height) * (1/1.61)
#     (width, height) = (int(im2.width * fraction),int( im2.height * fraction))
#     im_resized = im2.resize((width, height))

#     im1.paste(im_resized,(0,0),im_resized)
#     im1.save(app.config['UPLOAD_FOLDER']+ 'pdf/' + filename)


# if __name__ == "__main__":
#   app.run(host='0.0.0.0',debug=True, port=5000)
