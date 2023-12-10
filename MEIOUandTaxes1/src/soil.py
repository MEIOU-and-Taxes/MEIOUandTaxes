#!/usr/bin/env python -i

import os
import winsound
import sys
from PIL import Image

event_structure = """
country_event = {
	id = POP_Soil.%d
	title = "EVT_AI"
	desc = "EVT_AI"
	picture = MEIOU_AND_TAXES_eventPicture

	is_triggered_only = yes
	hidden = yes

	trigger = {
		always = yes
	}

	immediate = {%s
                %s
	}

	option = {
		name = "EVT_AI"
		ai_chance = { factor = 100 }
	}
}
"""
country_event = """
        country_event = {
            id = POP_Soil.%d
        }
"""

def parse_line(line):
	s = line.strip()
	ss = s.split('"')
	tokens = []
	for i,sss in enumerate(ss):
		if i%2==0:
			sss = sss.replace("="," = ").replace("{"," { ").replace("}"," } ")
			if "#" in sss:
				sss = sss.split("#")[0]
				tokens.extend(sss.split())
				return tokens
			tokens.extend(sss.split())
		else:
			tokens.append('"%s"' % sss)
	return tokens

def parse_file(fn):
	def update(dic, new):
		if isinstance(new, dict):
			new = new.items()
		for key, val in new:
			if key not in dic:
				dic[key] = val
			elif isinstance(dic[key], list):
				dic[key].append(val)
			else:
				dic[key] = [dic[key], val]
	d = {}
	names = []
	stack = [(d,"")]
	tokens = []
	key = ""
	with open(fn,"rb") as f:
		ff = f.read()
		try:
			fff = ff.decode("utf-8")
		except UnicodeDecodeError:
			fff = ff.decode("cp1252", errors="ignore")
		for line in fff.splitlines():
			tokens += parse_line(line)
		for token in tokens:
			if token == "=":
				key = names.pop()
			elif token == "{":
				dd = {}
				update(stack[-1][0], {key: dd})
				stack.append((dd,key))
				key = ""
			elif token == "}":
				if len(stack[-1][0]):
					update(stack.pop()[0], [(n,n) for n in names])
				else:
					k = stack.pop()[1]
					stack[-1][0][k] = []
					update(stack[-1][0], [(k,n) for n in names])
				names = []
			else:
				names.append(token)
				if key:
					update(stack[-1][0], {key: names.pop()})
					key = ""
	return d

def SetCoordToProv(image, colorToProv):
    return {(x, y):colorToProv[image.getpixel((x, y))] for x in range(image.width) for y in range(image.height)}

def SetColorToProv(defnt):
    colorToProv = {}
    lines = defnt.readlines()
    
    for line in lines[1:]:
            l = line.decode("latin-1").split(";")
            colorToProv[(int(l[1]), int(l[2]), int(l[3]))] = int(l[0])

    return colorToProv

def MakeEventFromList(lst1, lst2, provPerEvent=500):
    lstlst = []
    
    for prov in lst1:
        if prov % provPerEvent == 1:
            lstlst.append([prov])
        else:
            lstlst[-1].append(prov)

    op = 'namespace = POP_Soil\n\n'
    
    for lstlstlst in lstlst:
        tmpstr = '\n'

        for prov in lstlstlst:
            tmpstr += '\t\t%s\n' % ('%d = { set_variable = { which = Land_Soil value = %s } }' % (prov, str(round(lst2[prov], 3))))

        if lstlstlst == lstlst[-1]:
                op += event_structure % (lstlst.index(lstlstlst), tmpstr, '')
        else:
                op += event_structure % (lstlst.index(lstlstlst), tmpstr, country_event % (lstlst.index(lstlstlst) + 1))

    return op

if __name__ == "__main__":
    coordToProv = SetCoordToProv(Image.open('map\provinces.bmp'), SetColorToProv(open('map\definition.csv', 'rb')))

    soilLst = [[0, 0] for i in range(int(parse_file('map\default.map')['max_provinces']) + 1)]

    with Image.open('soil.png') as img:
        for y in range(img.height):
            if y % 100 == 0:
                print(y)
            for x in range(img.width):
                pxl = img.getpixel((x, y))

                if pxl == 11 or pxl == 6:
                    soilLst[coordToProv[(x, y)]][0] += 1
                    soilLst[coordToProv[(x, y)]][1] += 1
                elif pxl == 9 or pxl == 7 or pxl == 10:
                    soilLst[coordToProv[(x, y)]][0] += 2.5
                    soilLst[coordToProv[(x, y)]][1] += 1
                elif pxl == 8 or pxl == 4 or pxl == 3:
                    soilLst[coordToProv[(x, y)]][0] += 5
                    soilLst[coordToProv[(x, y)]][1] += 1
                    
        for i in soilLst:
            if i[1] > 0:
                soilLst[soilLst.index(i)] = i[0]/i[1]
            else:
                soilLst[soilLst.index(i)] = 1
                
        with open('events\POP_Soil.txt', 'w') as f:
            f.write(MakeEventFromList([i for i in range(len(soilLst))][1:], soilLst))
