import serial
import csv
import datetime

now = datetime.datetime.now()
now.strptime('20.12.2016 09:38:42,76', '%d.%m.%Y %H:%M:%S,%f')
path = r'C:\Users\klautens\PycharmProjects\Studienarbeit\exp_send'+'_'+str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)+'.csv'
f = open(path, 'w', newline='')
writer = csv.writer(f)
writer.writerow(("count", "time", "round", "poly_count", "total_bytes", "total_time", "rssi"))
ser = serial.Serial('COM3', 115200)
i = 0

try:
    while True:
        while ser.in_waiting:
            a = ser.readline().decode('utf-8')

            if a[0] == '1':

                print('Test')
                b = a.split('\r\n')[0].split(',')
                now = datetime.datetime.now()
                i = i+1
                writer.writerow((i, now, b[1], b[2], b[3], b[4], b[5]))
except KeyboardInterrupt:
    f.close()
    print("Terminated")
    pass






