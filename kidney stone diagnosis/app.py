from flask import Flask, render_template, request, redirect
import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from skimage import io
from tensorflow.keras.preprocessing import image


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # perform registration process (e.g. store in database)
        # ...
        
        # redirect to second page on successful registration
        return redirect('/success')
    
    # render registration form
    return render_template('register.html')

@app.route('/success',methods=['GET','POST'])
def success():

    return render_template('success.html')

@app.route('/index',methods=['GET','POST'])
def output():
    return render_template('/index.html')

model =tf.keras.models.load_model('mymodel.h5',compile=False)
# disease_class = ['probability of kidney stone in %','1','2']

def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(256, 256))
    show_img = image.load_img(img_path, grayscale=False, target_size=(256, 256))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    return preds


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        # Make prediction
        preds = model_predict(file_path, model)
        print(preds[0])

        # x = x.reshape([64, 64]);
        # disease_class = ['probability of kidney stone in %','1','2']
        # a = preds[0]
        ind=np.argmax(preds[0])
        print('Prediction:',ind)
        result=str(ind)
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
