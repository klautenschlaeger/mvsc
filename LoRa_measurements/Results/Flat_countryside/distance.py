import math

def converting(degs, minutes, seconds):
    deci_degrees = degs + minutes / 60 + seconds / 3600
    return deci_degrees

long2 = 11.907339166666667

lat2 = 50.61254888888889 #converting(degs=50, minutes=36, seconds=42.084)

print(long2)
print(lat2)

start_lon = converting(degs=11, minutes=54, seconds=24.692)
start_lat = converting(degs=50, minutes=36, seconds=48.842)

print(start_lon)
print(start_lat)
# start_lon = converting(degs=11, minutes=41, seconds=48.097)
# start_lat = converting(degs=52, minutes=23, seconds=58.029)




#haversine formula

R = 6378137.0
diff_lat_rad = (lat2 - start_lat) * math.pi / 180
diff_lon_rad = (long2 - start_lon) * math.pi / 180
a = math.sin(diff_lat_rad / 2) ** 2 + math.cos(start_lat) * math.cos(lat2) * (math.sin(diff_lon_rad / 2) ** 2)
c = 2 * math.atan2(math.sqrt(a), math.sqrt((1 - a)))
d = R * c
print(round(d, 3))
