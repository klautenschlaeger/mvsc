import time

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
app.config['SERIAL_PORT'] = '/dev/ttyUSB1'
app.config['SERIAL_BAUDRATE'] = 115200
app.config['SERIAL_BYTESIZE'] = 8
app.config['SERIAL_PARITY'] = 'N'
app.config['SERIAL_STOPBITS'] = 1

ser = Serial(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
polygon_id = 1

time_slot = 1

driver_id = 2
GROUP = [1, 2]
serialCommunicator = serialcommunicator.SerialCommunicator(driver_id)
preparerLoRa = preparerLoRaMessage.PrepareLoraMessage(driverId=driver_id, groups=GROUP)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    poly = []
    for i in range(0, 70, 1):
        poly.append([51.722475, 12.119768])
    update_own_polys(poly=poly)
    for msg in preparerLoRa.prepareBinaryMessages():
        handle_message(msg)
    return jsonify('pong!')


# communication flask/vue.js
@app.route('/mv', methods=['GET', 'POST'])
def all_machines():
    response_object = {'status': 'success'}
    global MACHINES
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
        response_object['message'] = 'Machine added!'
    else:
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
    print('needed:')
    print(response_data.get('needed'))
    pass


@scheduler.task('interval', id='do_job_1', seconds=10, start_date='2021-02-14 10:30:01')
def share_polygon_via_LoRa():
    for msg in preparerLoRa.prepareBinaryMessages():
        print(msg)
        time.sleep(0.100)
        ser.on_send(msg)


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
    # first case: self-produced poly
    structure = {
        "w_id": polygon_id,
        "d_id": driver_id,
        "w": poly
    }
    polygon_for_server = {'driverid': driver_id, 'workareaid': polygon_id, 'area': poly, 'groups': GROUP}
    # send_poly_to_central(polygon_for_server)
    OWN_POLYS.append(structure)
    preparerLoRa.addNewPoly(poly=poly, p_id=polygon_id)
    polygon_id = polygon_id + 1


def update_other_polys(structure, groups):
    print(structure)
    print(groups)
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
    app.run(host="localhost", port=5005, debug=True, use_reloader=False)
