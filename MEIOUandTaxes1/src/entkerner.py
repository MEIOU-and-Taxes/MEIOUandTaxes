import os
import codecs

fontfile = input("Input the font's filename here: ")
if fontfile == "":
	fontfile = "vic_18_black.fnt"
elif not ".fnt" in fontfile:
	fontfile += ".fnt"

locfile = input("Input the target localisation filename here: ")
if not ".yml" in locfile:
	locfile += ".yml"
locstart = int(input("Input the first line to entkern: "))
locend = int(input("Input the last line to entkern: "))
maxlen = input("Input the minimum output length in pixels: ")
if maxlen == "" or int(maxlen) < 1:
	maxlen = 0
else:
	maxlen = int(maxlen)

# fontfile = "vic_18_black.fnt"
# locfile = "test_l_english.yml"
# locstart = 2
# locend = 12
# maxlen = 0

fontfile = os.path.join("gfx", "fonts", fontfile)
if os.path.exists(os.path.join("localisation", "replace", locfile)):
	locfile = os.path.join("localisation", "replace", locfile)
else:
	locfile = os.path.join("localisation", locfile)

chardict = {} # id : xadvance
kerndict = {} # first : {second : amount, second : amount}
with open(fontfile, 'r') as fontf:
	font = [line.strip() for line in fontf.readlines()]
	data = [token for token in font[0].replace("  ", " ").split(" ")]
	for char in [line.split() for line in font if line.startswith("char id=")]:
		chardict[chr(int(char[1].split("=")[1]))] = int(char[8].split("=")[1])
	for kern in [line.split() for line in font if line.startswith("kerning first=")]:
		try:
			kerndict[chr(int(kern[1].split("=")[1]))][chr(int(kern[2].split("=")[1]))] = int(kern[3].split("=")[1])
		except KeyError:
			kerndict[chr(int(kern[1].split("=")[1]))] = dict([(chr(int(kern[2].split("=")[1])), int(kern[3].split("=")[1]))])


with codecs.open(locfile, 'r', encoding='utf-8-sig') as locf:
	loc = locf.readlines()
	editloc = [line.split("\"") for line in loc[locstart-1:locend]]
	newloc = []
	lengths = []
	for line in editloc:
		if len(line) > 2:
			length = 0
			lchar = None
			line = [line[0], "\"".join(line[1:-1]), line[-1]]

			for char in line[1]:
				length += chardict[char]
				try:
					length += kerndict[lchar][char]
				except KeyError:
					pass
				lchar = char
			if length > maxlen:
				maxlen = length
			lengths.append(length)
			newloc.append(line)
		else:
			lengths.append(-1)
			newloc.append(line)
	
	for x, line in enumerate(newloc):
		if lengths[x] >= 0:
			addlen = maxlen - lengths[x]
			while(addlen > 40):
				addlen -= 40
				line[1] += "£40px£"
			if(addlen > 0):
				line[1] += "£" + str(addlen) + "px£"
			loc[x + locstart - 1] = "\"".join(line)

with codecs.open(locfile, 'w', encoding='utf-8-sig') as locf:
	for line in loc:
		locf.write(line)
print("Output to " + locfile)
input()