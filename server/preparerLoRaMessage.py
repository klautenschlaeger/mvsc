import math
import struct


class PrepareLoraMessage(object):
    def __init__(self, driverId, groups):
        self.groups = groups
        self.driverId = driverId
        self.share_poly = []
        self.share_poly_ids = []

    def addNewPoly(self, poly, p_id):
        if poly.__len__() > 0:
            self.share_poly.append(poly)
        if type(p_id) == int:
            self.share_poly_ids.append(p_id)

    def reset_share_mem(self):
        self.share_poly = []
        self.share_poly_ids = []

    def prepareBinaryMessage(self, msg):
        id = self.driverId
        if self.driverId > 0:
            print("sharing ")
            if 1 in self.groups:
                id = id + 10000
            if 2 in self.groups:
                id = id + 2000
            if 3 in self.groups:
                id = id + 300
            element = 0
            for p in self.share_poly:
                poly = self.share_poly.pop(element)
                poly_int = []
                for coord in self.poly:
                    for coordinate in coord:
                        poly_int.append(int(coordinate * 10000000))
                p_id = self.share_poly_ids.pop(element)
                element = element + 1
                loads = math.ceil(len(poly_int) / 60)
                # print("loads: " + str(loads))
                # print("poly_int_len: " + str(poly_int.__len__()))
                poly_id = p_id * 100 + loads * 10
                for i in range(1, loads + 1, 1):
                    list_lora_int = [id, poly_id + i]
                    n = (i - 1) * 60
                    m = i * 60
                    # print(m)
                    # print(n)
                    if poly_int.__len__() - 1 < m:
                        m = poly_int.__len__()
                    # print(m)
                    list_lora_int = list_lora_int + poly_int[n:m]
                    buf = struct.pack('%si' % len(list_lora_int), *list_lora_int)
                    return buf
                    # print(list_lora_int)
                    # print("lora_int_len: " + str(list_lora_int.__len__()))
                    # print(buf)
