#!/usr/bin/env python

# WS server example

import asyncio
import struct

import requests
import websockets

url = 'http://localhost:5005/update/own'
waiting = []

async def hello(websocket, path):
    buffer = await websocket.recv()
    count_poly = struct.unpack_from("i", buffer=buffer, offset=0)
    # foreach poly in vecPoly
    print("count_poly: {0}".format(count_poly))
    if count_poly[0] == 100:
        message = []
        for byte in buffer:
            message.append(byte)
        message[0] = 1
        message_bytes = bytes(message)
        waiting.append(message_bytes)
        print(len(waiting))
    else:
        byte_to_area(count_poly[0], buffer=buffer)
        #await websocket.send(buffer)
        for msg in waiting:
            to_send = waiting.pop(0)
            await websocket.send(to_send)


def byte_to_area(count_poly, buffer):
    preheader = 0
    for a in range(0, count_poly, 1):
        header = struct.unpack_from("ii", buffer=buffer, offset=4 + a * 8 + 16 * preheader)
        print(header)
        coords2 = []
        # foreach coord in header[1] (east,north) decode:
        for i in range(0, header[1] * 2, 2):
            coordinate = []
            coordinate.append(
                float("{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=(12 + preheader * 16 + i * 8))[0])))
            coordinate.append(float(
                "{:.7f}".format(struct.unpack_from("d", buffer=buffer, offset=(12 + preheader * 16 + (i + 1) * 8))[0])))
            coords2.append(coordinate)
        print("coords2")
        print(coords2)
        print(coords2.__len__())
        preheader = header[1]
        field = {'area': coords2}
        x = requests.post(url, json=field)

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
