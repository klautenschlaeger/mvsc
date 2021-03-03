import asyncio
import math
import struct

import websockets


class SerialCommunicator(object):
    def __init__(self, driverId):
        self.driverId = driverId
        self.rev_polys = []
        self.available_structs = []

    def handleMessage(self, msg):
        print("handling message")
        converted_msg = []
        for b in struct.iter_unpack('i', msg):
            converted_msg.append(b[0])
        # G1 G2 G3 *100 #driver_id
        processing_driverID = converted_msg[0] % 100
        if processing_driverID == self.driverId and 0 < processing_driverID < 11:
            return None
        else:
            number = converted_msg[1] % 10
            if number == 1:
                self.rev_polys = []
            load = int((converted_msg[1] % 100 - number) / 10)
            if load == number:
                if load == 1:
                    # single packet
                    id = converted_msg.pop(0)
                    p_id = int((converted_msg.pop(0) - load * 10 - number) / 100)
                    self.convertPolyFormat(id=id, poly_id=p_id, poly=converted_msg)
                else:
                    # multiple packets
                    self.rev_polys.append(converted_msg)
                    id = converted_msg[0]
                    p_id = int((converted_msg[1] - load * 10 - number) / 100)
                    coords = []
                    no_wrong_packet = True
                    for packet in self.rev_polys:
                        rev_pid = int((packet[1] - packet[1] % 100) / 100)
                        current_id = packet[0]
                        if p_id == rev_pid and current_id == id:
                            converted_msg = packet
                            converted_msg.pop(0)
                            converted_msg.pop(0)
                            coords = coords + converted_msg
                        else:
                            rev_polys = []
                            no_wrong_packet = False
                            break
                    if no_wrong_packet:
                        self.convertPolyFormat(id=id, poly_id=p_id, poly=coords)
            else:
                self.rev_polys.append(converted_msg)

    def convertPolyFormat(self, id, poly_id, poly):
        driver = id % 100
        polygon = []
        # conversion to floats
        for e in poly:
            polygon.append(e / 10000000)
        coords = []
        # conversion to [[float,float]]
        for i in range(0, polygon.__len__(), 2):
            coordinate = []
            coordinate.append(float("{:.7f}".format(polygon[i])))
            coordinate.append(float("{:.7f}".format(polygon[i + 1])))
            coords.append(coordinate)
        structure = {
            "w_id": poly_id,
            "d_id": driver,
            "w": coords
        }
        groups = []
        id = id - driver
        id_group = int(math.floor(id / 10000))
        if id_group == 1 or id_group == 0:
            if id_group == 1:
                groups.append(1)
        else:
            return None
        id_group = int(math.floor(id / 1000)) % 10
        if id_group == 2 or id_group == 0:
            if id_group == 2:
                groups.append(2)
        else:
            return None
        id_group = int((id % 1000) / 100)
        if id_group == 3 or id_group == 0:
            if id_group == 3:
                groups.append(3)
        else:
            return None
        print("converting")
        print(structure)
        print(groups)
        self.available_structs.append((structure, groups))

    async def sendMessage(self, poly):
        poly_double = []
        if len(poly) > 0:
            for coordinate in poly:
                poly_double.append(coordinate[0])
                poly_double.append(coordinate[1])
        buf = struct.pack('iii', 100, 0, int(len(poly_double)))
        buf2 = struct.pack('%sd' % len(poly_double), *poly_double)
        total = buf + buf2
        uri = "ws://localhost:8770"
        async with websockets.connect(uri) as websocket:
            await websocket.send(total)

