import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
import scipy.stats
from PIL import Image

# used to pplot and evaluate received new and old polygons

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h, h

timeStamps = []
for a in range(0, 61, 6):
    timeStamps.append(a)
data = []


names = ["./mvsc2.csv", "./mvsc5.csv",  "./mvsc10.csv"]
legend = ["2 nodes in network", "5 nodes in network", "10 nodes in network"]
line_styles = ['-', '--', ':']
number = 3
s = 0
for name in names:
    stamps = []
    data = []
    with open(name, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for lines in csv_reader:
            if lines[1] == "vector":
                stamps.append(lines)
    for node in stamps:
        all = node[8].split(" ")
        numSent = []
        for i in range(0, len(all), 1):
            if i % 12 == number:
                asInt = int(all[i])
                if len(timeStamps) > len(numSent):
                    if asInt not in numSent:
                        numSent.append(asInt)
        data.append(numSent)
    data_average = []
    plot_data = []
    for i in range(0, 11, 1):
        temp_list = []
        for list1 in data:
            temp_list.append(list1[i])
        plot_data.append(temp_list)
    plot_data_processed = []
    for list2 in plot_data:
        plot_data_processed.append(mean_confidence_interval(list2))
    means = []
    mMinusH = []
    mPlusH = []
    hs = []
    for list3 in plot_data_processed:
        means.append(list3[0])
        mMinusH.append(list3[1])
        mPlusH.append(list3[2])
        hs.append(list3[3])
    #plt.plot(timeStamps, means, marker="x", linestyle=line_styles[s], label=legend[s], color="k")

    plt.errorbar(x=timeStamps, marker="x", y=means, yerr=hs, xerr=None, label=legend[s], fmt=line_styles[s],color="k", ecolor="k")
    s = s + 1
    #plt.fill_between(timeStamps, y1=mPlusH, y2=mMinusH)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
font = font_manager.FontProperties(family='Latin Modern',
                                   style='normal', size=16)

axis_font = font_manager.FontProperties(family='Latin Modern', size=16)
font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
plt.xlabel('time [min]', fontsize=16, fontdict=font)
# Set the y axis label of the current axis.
plt.ylabel('received old polygons \nper node',  fontsize=16, fontdict=font)
# show a legend on the plot
plt.tight_layout()
plt.legend(fontsize=16)
name = "rev_old"
path = r"./"
plt.savefig(path+name+".png", dpi=300, bbox_inches='tight')

"""
rgba = Image.open(path+name+".png")
rgb = Image.new('RGB', rgba.size, (255, 255, 255))  # white background
rgb.paste(rgba, mask=rgba.split()[3])               # paste using alpha channel as mask
rgb.save(path+name+".pdf", 'PDF', resoultion=100.0)
"""
