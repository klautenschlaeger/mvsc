import math


class DistanceCalculator(object):
    def __init__(self):
        self.centre = [0.0, 0.0]  # lat lon

    def calcDistance(self, centre_end):
        R = 6378137.0
        diff_lat_rad = (centre_end[0] - self.centre[0]) * math.pi / 180
        diff_lon_rad = (centre_end[1] - self.centre[1]) * math.pi / 180
        a = math.sin(diff_lat_rad / 2) ** 2 + math.cos(self.centre[0] * math.pi / 180) * math.cos(centre_end[0] * math.pi / 180) * (math.sin(diff_lon_rad / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt((1 - a)))
        d = R * c
        print(d)
        return round(d, 3)

    def calcCenter(self, poly):
        length = len(poly)
        east = 0.0
        north = 0.0
        for coord in poly:
            north = north + coord[0]
            east = east + coord[1]
        return [north/length, east/length]

    def setCentre(self, poly):
        self.centre = self.calcCenter(poly)
        print(self.centre)
