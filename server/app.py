from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

POLYS = [[],
         [],
         []
         ]
OWN_POLYS = []

GROUP = []

MACHINES = []
MACHINE = {}
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


driver_id = 0
"""
driver_id = 3
GROUP = [1, 2]
"""

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


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


def send_poly_to_central(post_data):
    response = requests.post('http://localhost:5001//mv/update', json=post_data)
    response_data = json.loads(response.text)
    print('needed:')
    print(response_data.get('needed'))
    pass


@app.route('/mv/update', methods=['POST'])
def update_polys():
    response_object = {'status': 'error'}
    post_data = request.get_json()
    driver = int(post_data.get('driverid'))
    #first case: self-produced poly
    if driver_id == driver:
        poly_id = post_data.get('workareaid')
        polygon = post_data.get('area')
        structure = {
            "w_id": poly_id,
            "d_id": driver,
            "w": polygon
        }
        send_poly_to_central(post_data)
        OWN_POLYS.append(structure)
        response_object = {'status': 'success'}
    else:
        groups = post_data.get("groups")
        same_group = False
        for e in groups:
            if e in GROUP:
                same_group = True;
                break
        if same_group:
            poly_id = post_data.get('workareaid')
            polygon = post_data.get('area')
            structure = {
                "w_id": poly_id,
                "d_id": driver,
                "w": polygon
            }
            for e in groups:
                if e in GROUP:
                    POLYS[e-1].append(structure)
            response_object = {'status': 'success'}
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(host="localhost", port=5005, debug=True)
