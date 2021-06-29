import csv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

file_name = "/home/karlo/Desktop/Studienarbeit/multipolygone_chursdorf_data_sample.csv"
stamps = []
with open(file_name, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for lines in csv_reader:
        stamps.append((lines[2], lines[3]))
stamps.pop(0)


numbers = []
for i in range(0, 76, 1):
    numbers.append(0)

for i in range(0, len(stamps), 1):
    start = int(stamps[i][0])
    stop = int(stamps[i][1])
    diff = stop - start
    numbers[diff] = numbers[diff] + 1


print(numbers)
print(numbers.__len__())







years = [str(a) for a in range(0, 76, 1)]
print(years)
visitors = (0, 0, 0, 0, 0, 35, 2, 8, 4, 13, 6, 7, 3, 4, 5, 5, 6, 7, 3, 18, 5, 17, 10, 25, 16, 22, 8, 37, 17, 33, 20, 25, 23, 20, 9, 21, 10, 11, 8, 9, 6, 6, 4, 5, 4, 4, 4, 2, 4, 5, 2, 2, 6, 3, 3, 3, 2, 5, 4, 6, 8, 11, 4, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0)
index = np.arange(len(years))
bar_width = 3.0
plt.figure(figsize=(6, 2))
plt.bar(index, numbers, bar_width,  color="green", )
x = np.arange(0, 76, 5)
print(x)

plt.xticks(x, fontsize=15)
plt.yticks(fontsize=15)
font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
plt.xlabel('Polygon creation interval [s]', fontsize=15, fontdict=font)
plt.ylabel('Number of\n polygons', fontsize=15, fontdict=font)
plt.tight_layout()

name = "timeint"
path = r"/home/karlo/Desktop/Studienarbeit/Latex/Bilder2/"
plt.savefig(path+name+".png", dpi=300, bbox_inches='tight')

rgba = Image.open(path+name+".png")
rgb = Image.new('RGB', rgba.size, (255, 255, 255))  # white background
rgb.paste(rgba, mask=rgba.split()[3])               # paste using alpha channel as mask
rgb.save(path+name+".pdf", 'PDF', resoultion=100.0)
