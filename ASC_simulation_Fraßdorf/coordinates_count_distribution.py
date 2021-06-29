import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager
matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
from PIL import Image

file_name = "/home/karlo/Desktop/Studienarbeit/Code/mvsc/ASC_simulation_Fraßdorf/multipolygone_chursdorf_data_sample.csv"
stamps = []
with open(file_name, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for lines in csv_reader:
        stamps.append(lines[0])
stamps.pop(0)

numbers = []


for i in range(0, len(stamps), 1):
    multi = stamps[i].split("(((")[1].split(")))")[0].split(",")
    length = multi.__len__()
    numbers.append(length)
    if 73 < length:
        print(length)

print(numbers)
print(numbers.__len__())


coord_count = [int(a) for a in range(0, 76, 1)]
print(coord_count)
plt.figure(figsize=(6, 2))
num_of_polygons = []
for coord in coord_count:
    num_of_polygons.append(numbers.count(coord))
index = np.arange(len(coord_count))
bar_width = 3.0
plt.bar(index, num_of_polygons, bar_width,  color="green")
x = np.arange(0, 76, 5)
print(x)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        }
plt.xlabel('Number of coordinates in a polygon', fontsize=15 , fontdict=font)


plt.ylabel('Number of\npolygons', fontsize=15, fontdict=font)
plt.xticks(x)# labels get centered
plt.tight_layout()


name = "coord_count"
path = r"./"
plt.savefig(path+name+".png", dpi=300, bbox_inches='tight')

rgba = Image.open(path+name+".png")
rgb = Image.new('RGB', rgba.size, (255, 255, 255))  # white background
rgb.paste(rgba, mask=rgba.split()[3])               # paste using alpha channel as mask
rgb.save(path+name+".pdf", 'PDF', resoultion=100.0)
