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
    if count_poly[0] == 100:
        message = []
        for byte in buffer:
            message.append(byte)
        message[0] = 1
        message_bytes = bytes(message)
        waiting.append(message_bytes)
        print(len(waiting))
    else:
        preheader = 0
        for a in range(0, count_poly[0], 1):
            header = struct.unpack_from("ii", buffer=buffer, offset=4 + a * 8 + 16 * preheader)
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
            field = {'area': coords2}
            x = requests.post(url, json=field)
            for msg in waiting:
                await websocket.send(msg)


start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
