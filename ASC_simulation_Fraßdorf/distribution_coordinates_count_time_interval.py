import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
import scipy.stats
from PIL import Image


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return [round(m, 4), round(m-h, 4), round(m+h, 4)]



file_name = "./multipolygone_chursdorf_data_sample.csv"
stamps = []

with open(file_name, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for lines in csv_reader:
        stamps.append((lines[0],lines[2], lines[3]))
stamps.pop(0)


data = []
time = []
time2 = []
for i in range(0, 76, 1):
    time.append([])



for i in range(0, len(stamps), 1):
    multi = stamps[i][0].split("(((")[1].split(")))")[0].split(",")
    length = multi.__len__()
    start = int(stamps[i][1])
    stop = int(stamps[i][2])
    diff = stop - start
    time[diff].append(length)

print(time)
for ele in time:
    if len(ele) > 1:
        time2.append(mean_confidence_interval(ele))
    else:
        time2.append(ele)
print(time2)
mean = []
timestamp = []
mPlusH = []
mMinusH = []
for index,ele in enumerate(time2,start=0):
    if len(ele) > 1:
        timestamp.append(index)
        mean.append(ele[0])
        mMinusH.append(ele[1])
        mPlusH.append(ele[2])
fig = plt.figure()
plt.plot(timestamp, mean, marker="o",  color="k")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
font = font_manager.FontProperties(family='Latin Modern',
                                   style='normal', size=16)

axis_font = font_manager.FontProperties(family='Latin Modern', size=16)
font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
plt.xlabel('Polygon creation interval [s]', fontsize=16, fontdict=font)
plt.ylabel('Number of coordinates in\n the polygon',  fontsize=16, fontdict=font)

plt.tight_layout()

plt.show()
'''
name = "dist2"
path = r"./"
plt.savefig(path+name+".png", dpi=300, bbox_inches='tight')

rgba = Image.open(path+name+".png")
rgb = Image.new('RGB', rgba.size, (255, 255, 255))  # white background
rgb.paste(rgba, mask=rgba.split()[3])               # paste using alpha channel as mask
rgb.save(path+name+".pdf", 'PDF', resoultion=100.0)
'''
