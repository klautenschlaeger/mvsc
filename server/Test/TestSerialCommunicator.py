import asyncio
import struct
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from serialcommunicator import SerialCommunicator as seriCommi


class TestSerialCommunicator(unittest.TestCase):
    def test_init(self):
        try:
            SeriCommiObj = seriCommi(driverId=1)
            asyncio.run(SeriCommiObj.sendMessage([[12.3456789, 12.3456789], [12.3456789, 12.3456789], [12.3456789, 12.3456789]]))
        except:
            self.fail("Class init threw an exeption")
        del SeriCommiObj

    def test_handling_own_msg(self):
        try:
            SeriCommiObj = seriCommi(driverId=1)
            buffer = []
            list_arrived = [12301, 1211]
            for i in range(0, 6, 1):
                list_arrived.append(123456789)
            buf = struct.pack("iiiiiiii", *list_arrived)
            SeriCommiObj.handleMessage(buf)
            self.assertEqual(SeriCommiObj.available_structs.__len__(), 0, "msg was handled even it is a own msg")
        except:
            self.fail("testing handling threw an exeption")
        del SeriCommiObj

    def test_handling_msg_groups(self):
        try:
            SeriCommiObj = seriCommi(driverId=1)
            buffer = []
            list_arrived = [12302, 1211]
            for i in range(0, 6, 1):
                list_arrived.append(123456789)
            buf = struct.pack("iiiiiiii", *list_arrived)
            SeriCommiObj.handleMessage(buf)
            self.assertEqual(SeriCommiObj.available_structs.__len__(), 1, "msg was not handled")
            self.assertEqual(SeriCommiObj.available_structs[0][1], [1, 2, 3], "Groups were processed wrong")
        except:
            self.fail("testing handling threw an exeption")
        del SeriCommiObj

    def test_handling_msg_groups2(self):
        try:
            SeriCommiObj = seriCommi(driverId=1)
            buffer = []
            list_arrived = [13302, 1211]
            for i in range(0, 6, 1):
                list_arrived.append(123456789)
            list_arrived[0] = 22302
            buf = struct.pack("iiiiiiii", *list_arrived)
            SeriCommiObj.handleMessage(buf)
            list_arrived[0] = 13302
            buf = struct.pack("iiiiiiii", *list_arrived)
            SeriCommiObj.handleMessage(buf)
            list_arrived[0] = 12402
            buf = struct.pack("iiiiiiii", *list_arrived)
            SeriCommiObj.handleMessage(buf)
            self.assertEqual(SeriCommiObj.available_structs.__len__(), 0, "group was handled wrong")

        except:
            self.fail("testing handling threw an exeption")
        del SeriCommiObj

    def test_handling_msg_coords(self):
        try:
            SeriCommiObj = seriCommi(driverId=1)
            buffer = []
            list_arrived = [12302, 1211]
            for i in range(0, 6, 1):
                list_arrived.append(123456789)
            buf = struct.pack("iiiiiiii", *list_arrived)
            SeriCommiObj.handleMessage(buf)
            self.assertEqual(SeriCommiObj.available_structs[0][0].get('w'), [[12.3456789, 12.3456789], [12.3456789, 12.3456789], [12.3456789, 12.3456789]],
                             "coords were handled wrong")
        except:
            self.fail("testing handling threw an exeption")
        del SeriCommiObj


if __name__ == '__main__':
    unittest.main()
