# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 21:38:18 2021

@author: Kunal Patel
"""
import os 
from flask import Flask, request
import json
from flask_cors import CORS
import base64

app = Flask(__name__)
cors = CORS(app)
datasetPath='data'

@app.route('/upload_canvas', methods=['POST'])
def upload_canvas():
    data= json.loads(request.data.decode('utf-8'))
    image_data = data['image'].split(',')[1].encode('utf-8')
    filename = data['filename']
    className = data['className']
    os.makedirs(f'{datasetPath}/{className}/image', exist_ok=True)
    with open(f'{datasetPath}/{className}/image/{filename}', 'wb') as fh:
        fh.write(base64.decodebytes(image_data))
        
    return "Got the image" + className    