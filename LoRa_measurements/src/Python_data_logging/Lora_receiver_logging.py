import serial
import csv
import datetime

now = datetime.datetime.now()
now.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f')
f = open('/home/karlo/Desktop/Studienarbeit/Code/Client_Server/thesis_client_server/src_py/wedo_data/exp_rec_1_3_' + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second) + ".csv", 'w', newline='')
writer = csv.writer(f)
writer.writerow(("time", "machine_id", "polygon_id", "rec_bytes", "rssi", "count_coords", "coords"))
ser = serial.Serial('/dev/ttyUSB0', 115200)
i = 0
while True:

    while ser.in_waiting:
        rec = ser.readline().decode('utf-8')
        if rec[0] == '1':
            print(rec)
            b = rec.split('\r\n')[0].split(',')
            print(b)
            #coords = b[6:]
            #print(coords)
            now = datetime.datetime.now()
            writer.writerow((now, b[1], b[2], b[3], b[4]))

