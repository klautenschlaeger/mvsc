import math
import struct


class PrepareLoraMessage(object):
    def __init__(self, driverId, groups):
        self.groups = groups
        self.driverId = driverId
        self.share_poly = []
        self.share_poly_ids = []

    def addNewPoly(self, poly, p_id):
        poly_int = []
        for coord in poly:
            for coordinate in coord:
                poly_int.append(int(coordinate * 10000000.0))
        self.share_poly.append(poly_int)
        self.share_poly_ids.append(p_id)

    def reset_share_mem(self):
        self.share_poly = []
        self.share_poly_ids = []

    def prepareBinaryMessages(self):
        id = self.driverId
        buffer = []
        if self.driverId > 0:
            if 1 in self.groups:
                id = id + 10000
            if 2 in self.groups:
                id = id + 2000
            if 3 in self.groups:
                id = id + 300
            element = 0
            for p in self.share_poly:
                poly_int = self.share_poly.pop(0)
                p_id = self.share_poly_ids.pop(0)
                element = element + 1
                loads = math.ceil(len(poly_int) / 60)
                poly_id = p_id * 100 + loads * 10
                for i in range(1, loads + 1, 1):
                    list_lora_int = [id, poly_id + i]
                    print("sharing: {0}".format(poly_id +i))
                    n = (i - 1) * 60
                    m = i * 60
                    if poly_int.__len__() - 1 < m:
                        m = poly_int.__len__()
                    list_lora_int = list_lora_int + poly_int[n:m]
                    buf = struct.pack('%si' % len(list_lora_int), *list_lora_int)
                    buffer.append(buf)
        return buffer
