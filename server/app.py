import time
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
import serialcommunicator
import preparerLoRaMessage
import asyncio

from flask_serial import Serial

from flask_apscheduler import APScheduler

POLYS = [[],
         [],
         []
         ]
OWN_POLYS = []

share_poly = []
share_poly_ids = []
scheduler = APScheduler()

MACHINES = []
MACHINE = {}
# configuration
DEBUG = False
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SERIAL_TIMEOUT'] = 0.2
app.config['SERIAL_PORT'] = '/dev/ttyUSB0'
app.config['SERIAL_BAUDRATE'] = 115200
app.config['SERIAL_BYTESIZE'] = 8
app.config['SERIAL_PARITY'] = 'N'
app.config['SERIAL_STOPBITS'] = 1

ser = Serial(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
polygon_id = 1

time_slot = 1


driver_id = 1
GROUP = [3]
serialCommunicator = serialcommunicator.SerialCommunicator(driver_id)
preparerLoRa = preparerLoRaMessage.PrepareLoraMessage(driverId=driver_id, groups=GROUP)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


# communication flask/vue.js
@app.route('/mv', methods=['GET', 'POST'])
def all_machines():
    response_object = {'status': 'success'}
    global MACHINES
    global GROUP
    if request.method == 'POST':
        global driver_id
        post_data = request.get_json()
        response = requests.post('http://localhost:5001/machine', json=post_data)
        response_data = json.loads(response.text)
        driver_id = response_data.get('driverid')
        MACHINE = {
            'id': driver_id,
            'drivername': post_data.get('drivername'),
            'forename': post_data.get('forename'),
            'machineid': post_data.get('machineid'),
            'one': post_data.get('one'),
            'two': post_data.get('two'),
            'three': post_data.get('three')
        }
        GROUP = []
        if post_data.get('one'):
            GROUP.append(1)
        if post_data.get('two'):
            GROUP.append(2)
        if post_data.get('three'):
            GROUP.append(3)
        preparerLoRa.groups = GROUP
        preparerLoRa.driverId = driver_id
        serialCommunicator.driverId = driver_id
        MACHINES = response_data.get('machines')
        print(MACHINES)
        response_object['message'] = 'Machine added!'
    else:
        post_data = {
            "group": GROUP
        }
        response2 = requests.post('http://localhost:5001/mv', json=post_data)
        response_data2 = json.loads(response2.text)
        MACHINES = response_data2.get("machines")
        response_object['machines'] = MACHINES
    return jsonify(response_object)


@app.route('/mv/poly', methods=['POST'])
def all_polys():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    counters = post_data.get('counters')
    print(counters)
    for i in range(0, 3, 1):
        coordinates = []
        if POLYS[i].__len__() > 0:
            if POLYS[i].__len__() > counters[i]:
                workareas = POLYS[i][counters[i]:]
                counters[i] = POLYS[i].__len__() - 1
                coordinates = []
                for e in workareas:
                    coordinates.append(e.get('w'))
        response_object['polys' + str(i + 1)] = coordinates
    coordinates = []
    if OWN_POLYS.__len__() > counters[3]:
        workareas = OWN_POLYS[counters[3]:]
        counters[3] = OWN_POLYS.__len__() - 1
        for e in workareas:
            coordinates.append(e.get('w'))
    response_object['polys_own'] = coordinates
    response_object['counters'] = counters
    return jsonify(response_object)


# communication with server
def send_poly_to_central(post_data):
    response = requests.post('http://localhost:5001/mv/update', json=post_data)
    response_data = json.loads(response.text)
    needed = response_data.get('needed')
    print('needed:')
    print(needed)
    if len(needed) > 0:
        loadNeeded(needed)
    pass


def loadNeeded(needed):
    to_request = []
    for identi in needed:
        d_id = identi % 100
        p_id = int((identi - d_id) / 100)
        found = False
        i = 0
        while not found and i < 3:
            for structure in POLYS[i]:
                if p_id == structure.get("w_id") and d_id == structure.get("d_id"):
                    found = True
                    break
            i = i + 1
        if not found:
            to_request.append(identi)

    post_data = {
        "needed": to_request
    }
    response = requests.post('http://localhost:5001/missing', json=post_data)
    response_data = json.loads(response.text)
    rev_polys = response_data.get("needed")
    for poly in rev_polys:
        structure = {
            "w_id": poly.get("w_id"),
            "d_id": poly.get("d_id"),
            "w": poly.get("w")
        }
        update_other_polys(structure=structure, groups=GROUP)


@scheduler.task('interval', id='do_job_1', seconds=10, start_date='2021-02-14 10:30:00')
def share_polygon_via_LoRa():
    for msg in preparerLoRa.prepareBinaryMessages():
        print("send_message!")
        print(msg)
        now = datetime.datetime.now()
        print("Current date and time : ")
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        ser.on_send(msg)
        time.sleep(0.50)


@app.route('/update/own', methods=['POST'])
def get_poly_from_QT():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    polygon = post_data.get('area')
    update_own_polys(polygon)
    return response_object


def update_own_polys(poly):
    global driver_id
    global polygon_id
    global GROUP
    global share_poly
    global share_poly_ids
    global preparerLoRa
    print(poly)
    # first case: self-produced poly
    structure = {
        "w_id": polygon_id,
        "d_id": driver_id,
        "w": poly
    }
    polygon_for_server = {'driverid': driver_id, 'workareaid': polygon_id, 'area': poly, 'groups': GROUP}
    OWN_POLYS.append(structure)
    #send_poly_to_central(polygon_for_server)
    preparerLoRa.addNewPoly(poly=poly, p_id=polygon_id)
    polygon_id = polygon_id + 1


def loadNeeded(needed):
    to_request = []
    global GROUP
    for identi in needed:
        d_id = identi % 100
        p_id = int((identi - d_id) / 100)
        found = False
        i = 0
        while not found and i < 3:
            for structure in POLYS[i]:
                if p_id == structure.get("w_id") and d_id == structure.get("d_id"):
                    found = True
                    break
            i = i + 1
        if not found:
            to_request.append(identi)
    post_data = {
        "needed": to_request
    }
    response = requests.post('http://localhost:5001/missing', json=post_data)
    response_data = json.loads(response.text)
    rev_polys = response_data.get("needed")
    for poly in rev_polys:
        structure = {
            "w_id": poly.get("w_id"),
            "d_id": poly.get("d_id"),
            "w": poly.get("w")
        }
        update_other_polys(structure=structure, groups=GROUP)


def update_other_polys(structure, groups):
    same_group = False
    for e in groups:
        if e in GROUP:
            same_group = True
            break
    if same_group:
        for e in groups:
            if e in GROUP:
                POLYS[e - 1].append(structure)
                asyncio.run(serialCommunicator.sendMessage(structure.get("w")))


@ser.on_message()
def handle_message(msg):
    serialCommunicator.handleMessage(msg)
    if len(serialCommunicator.available_structs) > 0:
        for element in serialCommunicator.available_structs:
            ele = serialCommunicator.available_structs.pop(0)
            update_other_polys(ele[0], ele[1])
        serialCommunicator.available_structs = []


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="localhost", port=5005, debug=True, use_reloader=False, threaded=True)

