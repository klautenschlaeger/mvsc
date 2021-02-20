#!/usr/bin/env python

# WS server example

import asyncio
import struct

import requests
import websockets

url = 'http://localhost:5005/update/own'


async def hello(websocket, path):
    buffer = await websocket.recv()
    count_poly = struct.unpack_from("i", buffer=buffer, offset=0)
    # foreach poly in vecPoly
    offset = 4
    print("count_poly: {0}".format(count_poly[0]))
    preheader = 0
    for a in range(0, count_poly[0], 1):
        header = struct.unpack_from("ii", buffer=buffer, offset=4 + a * 8 + 16 * preheader)
        print(header)


        coords2 = []
        # foreach coord in header[1] (east,north) decode:
        for i in range(0, header[1]*2, 2):
            coordinate = []
            coordinate.append(float("{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=(12 + preheader * 16 + i * 8))[0])))
            coordinate.append(float("{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=(12 + preheader * 16 + (i+1) * 8))[0])))
            coords2.append(coordinate)
        print("coords2")
        print(coords2)
        print(coords2.__len__())
        preheader = header[1]
        """
        coords1 = []
        # foreach coord in header[1] (east,north) decode:
        for i in range(0, header[1], 1):
            coordinate = []
            if i % 2 == 0:
                coordinate.append(float("{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=offset)[0])))
                offset = offset + 8
                coordinate.append(float("{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=offset)[0])))
                offset = offset + 8
                coords1.append(coordinate)
            else:
                offset = offset + 8
                coordinate.append(float("{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=(12 + (i + 1) * 8))[0])))
                offset = offset - 8
                coordinate.append(float("{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=(12 + i * 8))[0])))
                offset = offset + 16
                coords1.append(coordinate)
        rev_coords = []
        for i in range(1, len(coords1)+1, 1):
            rev_coords.append(coords1[len(coords1)-i])

        print(coords1)
        print(rev_coords)
        print(coords1.__len__())
        """
        field = {'area': coords2}
        x = requests.post(url, json=field)


start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
