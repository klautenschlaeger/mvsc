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
    if count_poly[0] > 1:
        for a in range(0, count_poly[0], 1):
            header = struct.unpack_from("ii", buffer=buffer, offset=offset)
            offset = offset + 8
            print(header)

            """
            coords2 = []
            # foreach coord in header[1] (east,north) decode:
            for i in range(0, header[1], 1):
                coordinate = []
                coordinate.append(float("{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=(12 + i * 8))[0])))
                coordinate.append(float("{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=(12 + (i+1) * 8))[0])))
                coords2.append(coordinate)
            print(coords2)
            print(coords2.__len__())
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
            print(coords1)
            print(coords1.__len__())
            field = {'area': coords1}
            x = requests.post(url, json=field)


start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
