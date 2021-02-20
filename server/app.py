from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
import serialcommunicator as SeriCommi
import preparerLoRaMessage

from flask_serial import Serial
import struct
import math
from flask_apscheduler import APScheduler

import asyncio
import websockets

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

# ser = Serial(app)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
polygon_id = 1

time_slot = 1

driver_id = 3
GROUP = [1, 2]
serialCommunicator = SeriCommi(driver_id)
preparerLoRa = preparerLoRaMessage(driver_id, GROUP)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    # asyncio.run(hello())
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
        print(driver_id)
        print(MACHINE)
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
    global driver_id
    global share_poly
    global share_poly_ids
    print("sharing ")
    id = driver_id
    if 1 in GROUP:
        id = id + 10000
    if 2 in GROUP:
        id = id + 2000
    if 3 in GROUP:
        id = id + 300
    element = 0
    for p in share_poly:
        poly = share_poly.pop(element)
        print(poly)
        poly_int = []
        for coord in poly:
            for coordinate in coord:
                poly_int.append(int(coordinate * 10000000))
        print(poly_int)
        p_id = share_poly_ids.pop(element)
        print(p_id)
        element = element + 1
        loads = math.ceil(len(poly_int) / 60)
        print("loads: " + str(loads))
        print("poly_int_len: " + str(poly_int.__len__()))
        poly_id = p_id * 100 + loads * 10
        for i in range(1, loads + 1, 1):
            list_lora_int = [id, poly_id + i]
            n = (i - 1) * 60
            m = i * 60
            print(m)
            print(n)
            if poly_int.__len__() - 1 < m:
                m = poly_int.__len__()
            print(m)
            list_lora_int = list_lora_int + poly_int[n:m]
            buf = struct.pack('%si' % len(list_lora_int), *list_lora_int)
            print(list_lora_int)
            print("lora_int_len: " + str(list_lora_int.__len__()))
            print(buf)
            # ser.on_send(buf)


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
    # first case: self-produced poly
    structure = {
        "w_id": polygon_id,
        "d_id": driver_id,
        "w": poly
    }
    polygon_for_server = {'driverid': driver_id, 'workareaid': polygon_id, 'area': poly, 'groups': GROUP}
    # send_poly_to_central(polygon_for_server)
    OWN_POLYS.append(structure)
    share_poly.append(poly)
    share_poly_ids.append(polygon_id)
    polygon_id = polygon_id + 1


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


# @ser.on_message()
def handle_message(msg):
    serialCommunicator.handleMessage(msg)
    if len(serialCommunicator.available_structs) > 0:
        for element in serialCommunicator.available_structs:
            update_other_polys(element[0], element[1])
        serialCommunicator.available_structs = []


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(host="localhost", port=5010, debug=True, use_reloader=False)
