from PIL import Image
import os

file = input('Enter image filename: ')
find = input('Enter "R G B" to find: ')

if "." not in file:
    file = file + ".bmp"

try:
    findimage = Image.open(file)
except IOError:
    print("File not found: " + file)
    input()
    quit()

try:
    mapimage = Image.open(os.path.join("map", "provinces.bmp"))
except IOError:
    print("Provinces.bmp not found")
    input()
    quit()

adjust = False
ratioadjust = float(findimage.width) / mapimage.width
if ratioadjust != 1.0:
    print("Image size is " + str(round(ratioadjust, 3)) + "x provinces.bmp  (" + str(findimage.width) + "px wide)")
    adjust = True

findimage = findimage.convert('RGB')

format = ("Red", "Green", "Blue")
find = find.split(" ")
for i, val in enumerate(find):
    try:
        val = int(val)
    except ValueError:
        try:
            val = float(val) * 255
            val = int(val)
        except ValueError:
            print("Invalid number for " + format[i] + ": " + val)
    find[i] = val

findtxt = " ".join([str(x) for x in find])
findcol = tuple(find)

colorprov = {}
with open(os.path.join("map", "definition.csv"), 'rb') as f:
    lines = f.readlines()
    for line in lines[1:]:
        l = line.decode("latin-1").split(";")
        colorprov[(int(l[1]), int(l[2]), int(l[3]))] = (l[4].strip(), l[0])

print("Reading input image...")

found = []
pix_x = 0
pix_y = 0

for rgb in findimage.getdata():
    if rgb == findcol:
        found.append((pix_x, pix_y))
    pix_x += 1
    if (pix_x == findimage.width):
        pix_x = 0
        pix_y += 1

if len(found) == 0:
    print("Color " + findtxt + " not found in source image.")
    input()
    quit()

print("Reading provinces.bmp...")

foundprovs = set()
pix_x = 0
pix_y = 0
n = len(found)
searching = found[0]
if adjust == True:
    for rgb in mapimage.getdata():
        if (int(round(pix_x * ratioadjust)), int(round(pix_y * ratioadjust))) == searching:
            foundprovs.add(colorprov[rgb])
            if n == 1:
                break
            n -= 1
            searching = found[len(found) - n]

        pix_x += 1
        if (pix_x == mapimage.width):
            pix_x = 0
            pix_y += 1
else:
    for rgb in mapimage.getdata():
        if (pix_x, pix_y) == searching:
            foundprovs.add(colorprov[rgb])
            if n == 1:
                break
            n -= 1
            searching = found[len(found) - n]

        pix_x += 1
        if (pix_x == mapimage.width):
            pix_x = 0
            pix_y += 1

for txt in foundprovs:
    print("Found in " + txt[0] + " (" + txt[1] + ")")
pass
input()
