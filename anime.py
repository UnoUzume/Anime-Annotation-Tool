from flask import Flask, render_template, Response, make_response, request, send_from_directory
from flask_cors import CORS
from pathlib import Path

from apps import api, creatProject
import apps.base

app = Flask(__name__,
            static_folder="./static",
            template_folder="./dist")
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)
app.register_blueprint(api, url_prefix='/api')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

apps.base.rootPath = Path(".")


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
    creatProject()
    print("run done")
    app.run(debug=True, use_reloader=False)
    # app.run(debug=True, threaded=True)
