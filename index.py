from io import StringIO
from flask import Flask, render_template, request, redirect, flash, url_for,send_file,send_from_directory,current_app
from flask.helpers import make_response, send_file
import main
import pdfkit
import urllib.request
from app import app
from werkzeug.utils import secure_filename
from main import getPrediction
import os
lis=[]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        lis.clear()
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            getPrediction(filename)
            label, path ,label1 = getPrediction(filename)
            flash(label)
            flash(filename)
            flash(label1)
            lis.append(label)
            lis.append(filename)
            lis.append(label1)
            return redirect('/')
        else:
            return render_template('error.html')
@app.route('/info')
def info():
    return render_template('acc.html')

@app.route('/download')
def download():
    if(len(lis)<3):
        return render_template('error.html')
    else:
        if("Not" in lis[2]):
            stat = "No, There is no Tumor"
            xx = "../static/happy.png"
        else:
            stat="Yes, Tumor is Present"
            xx = "../static/sad.jpg"
    return render_template('pdf.html',emot=xx,label=lis[0],label1=lis[2],filename="../static/"+lis[1],status=stat)
if __name__ == "__main__":
    app.run(host='0.0.0.0') 