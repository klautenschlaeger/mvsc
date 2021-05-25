import struct
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

from preparerLoRaMessage import PrepareLoraMessage as prepariLoRa


class TestSerialCommunicator(unittest.TestCase):
    def test_init(self):
        try:
            preLoRaObj = prepariLoRa(driverId=1, groups=[1, 2, 3])
        except:
            self.fail("Class init threw an exeption")
        del preLoRaObj

    def test_handling_own_msg(self):
        try:
            preLoRaObj = prepariLoRa(driverId=1, groups=[1, 2, 3])
            preLoRaObj.addNewPoly([[12.3456789, 12.3456789], [12.3456789, 12.3456789], [12.3456789, 12.3456789]], 12)
            self.assertEqual(preLoRaObj.share_poly.__len__(), preLoRaObj.share_poly_ids.__len__(), "poly was added wrong")
        except:
            self.fail("testing prepare threw an exeption")
        del preLoRaObj

    def test_handling_msg_groups(self):
        try:
            preLoRaObj = prepariLoRa(driverId=1, groups=[1, 2, 3])
            preLoRaObj.addNewPoly([[12.3456789, 12.3456789], [12.3456789, 12.3456789], [12.3456789, 12.3456789]], 12)
            preLoRaObj.reset_share_mem()
            self.assertEqual(preLoRaObj.share_poly.__len__(), preLoRaObj.share_poly_ids.__len__(), "poly was added wrong")
            self.assertEqual(preLoRaObj.share_poly.__len__(), 0, "poly was added wrong")
        except:
            self.fail("testing handling threw an exeption")
        del preLoRaObj



if __name__ == '__main__':
    unittest.main()
