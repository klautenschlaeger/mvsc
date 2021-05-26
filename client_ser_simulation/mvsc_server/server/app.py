from flask import Flask, jsonify, request
from flask_cors import CORS
import distanceCalculator

POLYS = [[],
         [],
         []]

GROUP = [[], [], [1, 2]]

MACHINES = [
    {
        'driverid': 1,
        'drivername': 'test',
        'forename': 'test',
        'machineid': 'John Deere 5430i_12',
        'one': False,
        'two': False,
        'three': True
    }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
disCalci = distanceCalculator.DistanceCalculator()

global driver_id
driver_id = 2


@app.route('/mv', methods=['GET', 'POST'])
def all_machines():
    response_object = {'status': 'success', 'machines': MACHINES}
    return jsonify(response_object)


@app.route('/machine', methods=['POST'])
def new_machines():
    response_object = {'status': 'success'}
    global driver_id
    post_data = request.get_json()
    MACHINES.append({
        'driverid': driver_id,
        'drivername': post_data.get('drivername'),
        'forename': post_data.get('forename'),
        'machineid': post_data.get('machineid'),
        'one': post_data.get('one'),
        'two': post_data.get('two'),
        'three': post_data.get('three')
    })
    response_object['driverid'] = driver_id
    MACHINES2 = [{
        'driverid': driver_id,
        'drivername': post_data.get('drivername'),
        'forename': post_data.get('forename'),
        'machineid': post_data.get('machineid'),
        'one': post_data.get('one'),
        'two': post_data.get('two'),
        'three': post_data.get('three')
    }]
    ids = [driver_id]
    if post_data.get('one'):
        GROUP[0].append(driver_id)
    if post_data.get('two'):
        GROUP[1].append(driver_id)
    if post_data.get('three'):
        GROUP[2].append(driver_id)
    for machine in MACHINES:
        if post_data.get('one'):
            if machine.get('one'):
                if machine.get("driverid") not in ids:
                    MACHINES2.append(machine)
                    ids.append(machine.get('driverid'))
        if post_data.get('two'):
            if machine.get('two'):
                if machine.get("driverid") not in ids:
                    MACHINES2.append(machine)
                    ids.append(machine.get('driverid'))
        if post_data.get('three'):
            if machine.get('three'):
                if machine.get("driverid") not in ids:
                    MACHINES2.append(machine)
                    ids.append(machine.get("driverid"))
    response_object['message'] = 'Machine added!'
    response_object['machines'] = MACHINES2
    driver_id = driver_id + 1
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
    response_object['counters'] = counters
    return jsonify(response_object)


@app.route('/mv/update', methods=['POST'])
def update_polys():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    driver = int(post_data.get('driverid'))
    poly_id = post_data.get('workareaid')
    polygon = post_data.get('area')
    centre = disCalci.calcCenter(poly=polygon)
    structure = {
        "w_id": poly_id,
        "d_id": driver,
        "w": polygon,
        "centre": centre
    }
    needed = []
    disCalci.setCentre(polygon)
    for i in range(0, 3, 1):
        if driver in GROUP[i]:
            if POLYS[i].__len__() > 0:
                for poly in POLYS[i]:
                    if poly.get("d_id") != driver:
                        distance = disCalci.calcDistance(centre_end=poly.get("centre"))
                        if distance < 150:
                            print(distance)
                            code = poly.get("w_id") * 100 + poly.get("d_id")
                            if code not in needed:
                                needed.append(code)
            POLYS[i].append(structure)
    response_object['needed'] = needed
    return jsonify(response_object)


@app.route('/missing', methods=['POST'])
def send_polys():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    needed = post_data.get('needed')
    needed_polys = []
    for code in needed:
        driver = code % 100
        p_id = int((code - driver)/100)
        found = False
        i = 0
        while not found and i < 3:
            for structure in POLYS[i]:
                if structure.get("d_id") == driver and structure.get("w_id") == p_id:
                    needed_polys.append(structure)
                    found = True
                    break
            i = i + 1
    response_object["needed"] = needed_polys
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)
