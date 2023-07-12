from flask import Flask,render_template,url_for,request,redirect,flash
from werkzeug.utils import secure_filename
import os
import pefile
import numpy as np
from PIL import Image
import cv2



app = Flask(__name__)

UPLOAD_FOLDER = '/home/madhudimple/RuTAG/Upload_file'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['exe', 'bin','png'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            #print('upload_image filename: ' + filename)
            flash('Image successfully uploaded and displayed below')

            pe = pefile.PE(filepath)

            # Extract the binary data from the executable
            binary_data = bytes(pe.get_memory_mapped_image())

            # Determine image dimensions based on the binary data size
            width = int(np.sqrt(len(binary_data)))
            height = len(binary_data) // width

            # Create a 1D NumPy array from the binary data
            arr = np.frombuffer(binary_data, dtype=np.uint8)

            # Reshape the array to match the image dimensions
            arr = arr[:width * height]  # Truncate excess data if necessary
            arr = arr.reshape((height, width))

            # Create an image from the NumPy array
            image = Image.fromarray(arr)

            # Save the image
            cnv_image = '/home/madhudimple/RuTAG/Converted_image'
            image_path = os.path.join(cnv_image,filename)
            image.save(image_path)

            image = cv2.imread(image_path)
            gray = cv2.resize(image,(128,128))
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
            image = np.expand_dims(image,axis=0)


            #predict ransomware class


            return render_template('next.html',)

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
