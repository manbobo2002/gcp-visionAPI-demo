from __future__ import division, print_function
# coding=utf-8
import sys
import io
import os
import glob
import re
import numpy as np

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


# Instantiates a client
client = vision.ImageAnnotatorClient()


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# You can also use pretrained model from Keras
# Check https://keras.io/applications/


def model_predict(img_path):

    print(img_path)
    file_name = os.path.abspath(img_path)
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print(labels)

    return labels


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path)

        output=""
        for label in preds:
            print(label.description)
            if label == preds[-1]:
                output=output+label.description+" with "+str(label.score)
            else:
                output=output+label.description+" with "+str(label.score)+","
        return output
    return None


if __name__ == '__main__':
    # app.run(port=5002, debug=True)

    # Serve the app with gevent
    #http_server = WSGIServer(('0.0.0.0', 5000), app)
    #http_server.serve_forever()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    