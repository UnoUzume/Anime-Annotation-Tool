from flask import Flask, render_template, Response, make_response, request, send_from_directory
from furl import furl
import requests
from datetime import timedelta
import time
import io
import re
import zlib
import base64
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image
from cv2 import cv2

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/<filename>', methods=['GET'])
def getStaticFile(filename: str):
    response = send_from_directory('./dist', filename)
    if filename.endswith("js"):
        response.headers['Content-Type'] = 'text/javascript'
    return response


@app.route('/assets/<filename>', methods=['GET'])
def getAssets(filename: str):
    response = send_from_directory('./dist/assets', filename)
    if filename.endswith("js"):
        response.headers['Content-Type'] = 'text/javascript'
    return response


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, threaded=True)
