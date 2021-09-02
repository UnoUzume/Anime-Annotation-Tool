from flask import Flask, render_template, Response, make_response, request
from flask import Blueprint, render_template, request, jsonify, current_app, flash, g
from concurrent.futures import ThreadPoolExecutor
import json
import base64
import time
from .project import Project
from .base import Patha

api = Blueprint("api", __name__, template_folder="templates")
project: Project = None

executor = ThreadPoolExecutor()


@api.route('/')
def index():
    return "opencv api"


@api.route('/creatproject')
def creatProject():
    global project
    # print(str(Patha("config.json").resolve()))
    with Patha("config.json").open(encoding="UTF-8") as f:
        project = Project(json.load(f))
    print("creatproject done")
    return "creatproject done"


@api.route('/frame/<int:frameNum>', methods=['GET', 'POST'])
def get_frame(frameNum):
    # frameNum = int(frameNum)
    for _ in range(20):
        time.sleep(0.2)
        imageData = project.video1.getBytes(frameNum)
        if imageData is not None:
            executor.submit(project.video1.preGet, frameNum)
            response = make_response(imageData)
            response.headers['Content-Type'] = 'image/png'
            return response


@api.route('/send/<task>', methods=['POST'])
def send(task):
    # if request.method == 'POST':
    if task == "get_frame":
        project.frameNum_gj = int(request.json['frameNum'])
        return "get_frame ok"
    elif task == "gen_water":
        if 'mask_canvas_b64' in request.json:
            time_start = time.time()

            mCan_comped = base64.b64decode(request.json['mask_canvas_b64'])
            cWater_comped = project.genWater(mCan_comped)
            base64_str = base64.b64encode(cWater_comped).decode('ascii')

            time_end = time.time()
            print("gen mask: "+str(time_end-time_start))
            return base64_str
        return "gen_water error"


@api.route('/get', methods=['POST'])
def get():
    return jsonify(project.getAttr(request.json['keys']))


def event_stream():
    while project.video2.ana_keyframes_lock <= 2:
        time.sleep(0.2)
        if project.video2.ana_keyframes_lock == 1:
            project.video2.ana_keyframes_lock = 0
            yield 'data: %s/%s %s\n\n'\
                % (project.video2.keyframes[-1],
                   project.video2.frames_tatal,
                   project.video2.keyframes[-1]-project.video2.keyframes[-2] if len(project.video2.keyframes) > 1 else 0)
        elif project.video2.ana_keyframes_lock == 2:
            project.video2.ana_keyframes_lock = 3
            project.video1.keyframes = project.video2.keyframes
            print("yield end")
            yield 'event: yield_end\ndata: tatal keyframes: %s\n\n' % len(project.video2.keyframes)


@api.route('/ana_keyframes', methods=['GET', 'POST'])
def ana_keyframes():
    executor.submit(project.video2.ana_keyframes_process)
    return Response(event_stream(), mimetype="text/event-stream")
