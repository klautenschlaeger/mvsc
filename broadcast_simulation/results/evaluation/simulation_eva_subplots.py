import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
import scipy.stats
from PIL import Image

# used to pplot and evaluate send new and old polygons

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
number = 0
means_total = []
mMinusH_total = []
mPlusH_total = []
hs_total = []

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
    means_total.append(means)
    mPlusH_total.append(mPlusH)
    mMinusH_total.append(mMinusH)
    hs_total.append(hs)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
ax1.errorbar(x=timeStamps, marker="x", y=means_total[0], yerr=hs_total[0], xerr=None, label=legend[0], fmt=line_styles[0], color="k",
             ecolor="k")

ax2.errorbar(x=timeStamps, marker="x", y=means_total[1], yerr=hs_total[1], xerr=None, label=legend[1], fmt=line_styles[1], color="k",
             ecolor="k")
ax3.errorbar(x=timeStamps, marker="x", y=means_total[1], yerr=hs_total[2], xerr=None, label=legend[2], fmt=line_styles[1], color="k",
             ecolor="k")

font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
ax1.set_xlabel('(a) time [min]', fontsize=17, fontdict=font)
ax2.set_xlabel('(b) time [min]', fontsize=17, fontdict=font)
ax3.set_xlabel('(c) time [min]', fontsize=17, fontdict=font)
ax1.set_ylabel('sent new polygons \nper node', fontsize=17, fontdict=font)
ax1.tick_params(labelsize=17)
ax2.tick_params(labelsize=17)
ax3.tick_params(labelsize=17)
plt.tight_layout()
font = font_manager.FontProperties(family='Latin Modern',
                                   style='normal', size=16)

axis_font = font_manager.FontProperties(family='Latin Modern', size=16)
font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }



plt.show()

name = "sent_new"
path = r"./"
fig.savefig(path+name+".png", dpi=300, bbox_inches='tight')

rgba = Image.open(path+name+".png")
rgb = Image.new('RGB', rgba.size, (255, 255, 255))  # white background
rgb.paste(rgba, mask=rgba.split()[3])               # paste using alpha channel as mask
rgb.save(path+name+".pdf", 'PDF', resoultion=100.0)

