import csv
import numpy as np
import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return round(m, 4), round(m-h, 4), round(m+h, 4)


rssi = []

file_rev = "exp_rec_2_2_11_11_55.csv"
with open(file_rev, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for line in csv_reader:
        rssi_value = int(line[4])
        if rssi_value > -150:
            rssi.append(rssi_value)

print(mean_confidence_interval(rssi))
