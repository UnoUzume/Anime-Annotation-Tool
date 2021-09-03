from flask import Flask, render_template, Response, make_response, request
from flask import Blueprint, render_template, request, jsonify, current_app, flash, g
from concurrent.futures import ThreadPoolExecutor
import json
import base64
import time
import importlib
from .project import Project
from .base import Patha

api = Blueprint("api", __name__, template_folder="templates")
myproject: Project = None

executor = ThreadPoolExecutor()


@api.route('/')
def index():
    return "opencv api"


@api.route('/creatproject')
def creatProject():
    global myproject
    # print(str(Patha("config.json").resolve()))
    importlib.reload(project)
    from .project import Project
    with Patha("config.json").open(encoding="UTF-8") as f:
        myproject = Project(json.load(f))
    print("creatproject done")
    return "creatproject done"


@api.route('/frame/<int:frameNum>', methods=['GET', 'POST'])
def get_frame(frameNum):
    # frameNum = int(frameNum)
    for _ in range(20):
        time.sleep(0.2)
        imageData = myproject.video1.getBytes(frameNum)
        if imageData is not None:
            executor.submit(myproject.video1.preGet, frameNum)
            response = make_response(imageData)
            response.headers['Content-Type'] = 'image/png'
            return response


@api.route('/send/<task>', methods=['POST'])
def send(task):
    # if request.method == 'POST':
    if task == "getframe":
        myproject.frameNum_gj = int(request.json['frameNum'])
        return "getframe ok"
    elif task == "getframe0":
        frameNum = request.json['frameNum']
        cCan_comped = base64.b64decode(request.json['cCanData_b64'])
        mCan_comped = base64.b64decode(request.json['mCanData_b64'])
        cCan_comped, mCan_comped = myproject.getframe0(
            frameNum, cCan_comped, mCan_comped)
        cWater_comped = myproject.genWater(mCan_comped)
        cCanData_b64 = base64.b64encode(cCan_comped).decode('ascii')
        mCanData_b64 = base64.b64encode(mCan_comped).decode('ascii')
        cWaterData_b64 = base64.b64encode(cWater_comped).decode('ascii')
        return jsonify({"cCanData_b64": cCanData_b64, "mCanData_b64": mCanData_b64, "cWaterData_b64": cWaterData_b64})
    elif task == "gen_water":
        time_start = time.time()

        mCan_comped = base64.b64decode(request.json['mCanData_b64'])
        cWater_comped = myproject.genWater(mCan_comped)
        base64_str = base64.b64encode(cWater_comped).decode('ascii')

        time_end = time.time()
        print("gen mask: "+str(time_end-time_start))
        return base64_str


@api.route('/get', methods=['POST'])
def get():
    return jsonify(myproject.getAttr(request.json['keys']))


def event_stream():
    while myproject.video2.ana_keyframes_lock <= 2:
        time.sleep(0.2)
        if myproject.video2.ana_keyframes_lock == 1:
            myproject.video2.ana_keyframes_lock = 0
            yield 'data: %s/%s %s\n\n'\
                % (myproject.video2.keyframes[-1],
                   myproject.video2.frames_tatal,
                   myproject.video2.keyframes[-1]-myproject.video2.keyframes[-2] if len(myproject.video2.keyframes) > 1 else 0)
        elif myproject.video2.ana_keyframes_lock == 2:
            myproject.video2.ana_keyframes_lock = 3
            myproject.video1.keyframes = myproject.video2.keyframes
            print("yield end")
            yield 'event: yield_end\ndata: tatal keyframes: %s\n\n' % len(myproject.video2.keyframes)


@api.route('/ana_keyframes', methods=['GET', 'POST'])
def ana_keyframes():
    executor.submit(myproject.video2.ana_keyframes_process)
    return Response(event_stream(), mimetype="text/event-stream")
