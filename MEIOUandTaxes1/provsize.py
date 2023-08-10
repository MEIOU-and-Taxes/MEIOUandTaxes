#!/usr/bin/env python -i

# Paradox file parsers and utilities for loading EU4 province sizes and positions
# by seboden 2017

event_structure = """
country_event = {
    id = distance_calc.%d
    title = no_localisation
    desc = no_localisation
    picture = MEIOU_AND_TAXES_eventPicture

    is_triggered_only = yes
    hidden = yes

    immediate = {%s
    }

    option = {
        name = no_localisation
    }
}
"""

import os
import sys
import math

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
        fff = ff.decode("iso-8859-1")
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

def get_provgroup(f, op):
    for group in f:
        if len(f[group]) > 0:
            op[f[group][0]] = f[group][0:]

def calc_provgroup(f, n):
    ind = 0

    output1 = '%sgroup = {\n\t' % n
    output2 = ''
        
    for item in f:
        ind += 1

        output1 += '%s ' % item
        output2 += '%s_%d = {\n\t' % (n, ind)

        for prov in f[item]:
            output2 += '%s ' % prov

        output2 += '\n}\n'

    output1 += '\n}\n\n'

    return output1, output2

def calc_partgroup(f, ff, n, nn):
    ind = 0

    output = ''
        
    for item in f:
        ind += 1
                
        output += '%s_%d_%s = {\n\t' % (n, ind, nn)
       
        for prov in f[item]:
            for center in ff:
                if prov == center:
                    output += '%s ' % prov

                    break

        output += '\n}\n'

    return output

def add_provgroup(path, sea_prov):
    r = parse_file(os.path.join(path, 'region.txt'))
    a = parse_file(os.path.join(path, 'area.txt'))
    s = parse_file(os.path.join(path, 'superregion.txt'))
    c = parse_file(os.path.join(path, 'continent.txt'))

    for region in r:
        if region == 'valhalla_region' or region == 'adventure_region':
            r[region] = []
    
    for region in r:
        if 'areas' in r[region]:
            tl = []
                        
            for area in r[region]['areas']:
                if int(a[area][0]) in sea_prov:
                    tl = []
                                        
                    break
                tl.extend(a[area])
                                
            r[region] = list(tl)
        else:
            r[region] = []

    for sr in s:
        tl = []

        for region in s[sr]:
            tl.extend(r[region])

        s[sr] = list(tl)

    for cont in c:
        if cont == 'new_world' or cont == 'island_check_provinces' or cont == 'antarctica':
            c[cont] = []

    region = {}
    superregion = {}
    cont = {}

    get_provgroup(r, region)
    get_provgroup(s, superregion)
    get_provgroup(c, cont)
        
    with open(os.path.join(path, "provincegroup.txt"), encoding='ISO-8859-1') as ff:
        t = ff.read()
        t = t[:t.find('portgroup')].rstrip('\n\t ') + '\n\n'
        portgroup = 'portgroup = {\n'
        
        i = 0

        for port in sea_prov:
            if i == 0:
                portgroup += '\t'
                                    
            portgroup += '%d ' % port

            i += 1

            if i == 20:
                i = 0

                portgroup += '\n'

        portgroup += '\n}\n\n'

        regiongroup, regionpart = calc_provgroup(region, 'region')
        srgroup, srpart = calc_provgroup(superregion, 'sr')
        contgroup, contpart = calc_provgroup(cont, 'cont')

        contregion = calc_partgroup(cont, region, 'cont', 'region')
        
        with open(os.path.join(path, "provincegroup.txt"), 'w', encoding='ISO-8859-1') as fff:
            fff.write('%s%s%s%s%s%s%s%s' % (t, portgroup, regiongroup, srgroup, contgroup, srpart, contpart, contregion))

def mapjoin(path):
    return os.path.join('map', path)

def province_stats(path="", compute_from_map=True, prov_per_event=500):
    """The compute_from_map option is computationally intensive, but corrects the distortion of province sizes by the map projection;
     it also computes all river connections between provinces 
     prov_per_event specifies how many provinces are set per setup event"""
    
    comment = """namespace = distance_calc
# Event to set the size (in pixels)  and coordinates of all provinces as variables;
# also save the square root of the size as an approximation of distance and travel times;
# also save all river_connections as province_flags ("river_province" and "river_to_####")"""
    
    default_map = parse_file(os.path.join(path, "default.map"))
    positions = parse_file(os.path.join(path, "positions.txt"))
    climate = parse_file(os.path.join(path, "climate.txt"))
    
    provnumber = int(default_map["max_provinces"])
    provcolor = {}
    with open(os.path.join(path, "definition.csv"), 'rb') as f:
        lines = f.readlines()
        for line in lines[1:]:
            l = line.decode("latin-1").split(";")
            provcolor[int(l[0])] = (int(l[1]), int(l[2]), int(l[3]))
    
    from PIL import Image
    
    mapimage = Image.open(os.path.join(path, "provinces.bmp"))
    colorsize = {rgb: count for count, rgb in mapimage.getcolors(256**3)}
    
    riverconnections = {}

    coordToProv = SetCoordToProv(Image.open(mapjoin('provinces.bmp')), SetColorToProv(open(mapjoin('definition.csv'), 'rb')))

    soilLst = [[0, 0] for i in range(int(parse_file(mapjoin('default.map'))['max_provinces']) + 1)]
    heatAvgLst = [[0, 0] for i in range(int(parse_file(mapjoin('default.map'))['max_provinces']) + 1)]
    heatDailyLst = [[0, 0] for i in range(int(parse_file(mapjoin('default.map'))['max_provinces']) + 1)]
    heatSeasonalLst = [[0, 0] for i in range(int(parse_file(mapjoin('default.map'))['max_provinces']) + 1)]
    rainLst = [[0, 0] for i in range(int(parse_file(mapjoin('default.map'))['max_provinces']) + 1)]
    inunLst = [[0, 0] for i in range(int(parse_file(mapjoin('default.map'))['max_provinces']) + 1)]

    with Image.open('soil.png') as img:
        for y in range(img.height):
            for x in range(img.width):
                pxl = img.getpixel((x, y))

                soilLst[coordToProv[(x, y)]][0] += pxl / 7
                soilLst[coordToProv[(x, y)]][1] += 1

    img = Image.open('AverageRange.png')
    rgb2temp = dict()

    y = 36

    for x in range(0, 1248):
        rgb2temp[img.getpixel((x, y))] = x * 51 / 1248 - 20

    rgbs = [i for i in rgb2temp]
    
    with Image.open('AvgTemp.png') as img:
        for y in range(img.height):
            for x in range(img.width):
                pxl = img.getpixel((x, y))

                if pxl in rgb2temp:
                    heatAvgLst[coordToProv[(x, y)]][0] += rgb2temp[pxl]
                    heatAvgLst[coordToProv[(x, y)]][1] += 1
                elif pxl != (0, 0, 0):
                    mn = [(rgb[0] - pxl[0])**2 + (rgb[1] - pxl[1])**2 + (rgb[2] - pxl[2])**2 for rgb in rgbs]
                    rgb2temp[pxl] = rgb2temp[rgbs[mn.index(min(mn))]]
                    
                    heatAvgLst[coordToProv[(x, y)]][0] += rgb2temp[pxl]
                    heatAvgLst[coordToProv[(x, y)]][1] += 1

    img = Image.open('DailyRange.png')
    rgb2temp2 = dict()

    y = 36

    for x in range(0, 2004):
        rgb2temp2[img.getpixel((x, y))] = x * 20 / 2004

    rgbs2 = [i for i in rgb2temp2]
    
    with Image.open('DailyTemp.png') as img:
        for y in range(img.height):
            for x in range(img.width):
                pxl = img.getpixel((x, y))

                if pxl in rgb2temp2:
                    heatDailyLst[coordToProv[(x, y)]][0] += rgb2temp2[pxl]
                    heatDailyLst[coordToProv[(x, y)]][1] += 1
                elif pxl != (0, 0, 0):
                    mn = [(rgb[0] - pxl[0])**2 + (rgb[1] - pxl[1])**2 + (rgb[2] - pxl[2])**2 for rgb in rgbs2]
                    rgb2temp2[pxl] = rgb2temp2[rgbs2[mn.index(min(mn))]]
                    
                    heatDailyLst[coordToProv[(x, y)]][0] += rgb2temp2[pxl]
                    heatDailyLst[coordToProv[(x, y)]][1] += 1

    img = Image.open('SeasonalRange.png')
    rgb2temp3 = dict()

    y = 36

    for x in range(0, 2061):
        rgb2temp3[img.getpixel((x, y))] = x * 58 / 2061

    rgbs3 = [i for i in rgb2temp3]
    
    with Image.open('SeasonalTemp.png') as img:
        for y in range(img.height):
            for x in range(img.width):
                pxl = img.getpixel((x, y))

                if pxl in rgb2temp3:
                    heatSeasonalLst[coordToProv[(x, y)]][0] += rgb2temp3[pxl]
                    heatSeasonalLst[coordToProv[(x, y)]][1] += 1
                elif pxl != (0, 0, 0):
                    mn = [(rgb[0] - pxl[0])**2 + (rgb[1] - pxl[1])**2 + (rgb[2] - pxl[2])**2 for rgb in rgbs3]
                    rgb2temp3[pxl] = rgb2temp3[rgbs3[mn.index(min(mn))]]
                    
                    heatSeasonalLst[coordToProv[(x, y)]][0] += rgb2temp3[pxl]
                    heatSeasonalLst[coordToProv[(x, y)]][1] += 1
    
    img = Image.open('RainfallScale_simple.png')
    rgb2temp4 = dict()
    
    y = 124
    
    for x in range(26, 1518):
        rgb2temp4[img.getpixel((x, y))] = (x - 26) / 1491

    rgbs4 = [i for i in rgb2temp4]
    
    
    with Image.open('Rainfall_simple.png') as img:
        for y in range(img.height):
            for x in range(img.width):
                pxl = img.getpixel((x, y))

                if pxl in rgb2temp4:
                    rainLst[coordToProv[(x, y)]][0] += rgb2temp4[pxl]
                    rainLst[coordToProv[(x, y)]][1] += 1
                elif pxl != (0, 0, 0):
                    mn = [(rgb[0] - pxl[0])**2 + (rgb[1] - pxl[1])**2 + (rgb[2] - pxl[2])**2 for rgb in rgbs4]
                    rgb2temp4[pxl] = rgb2temp4[rgbs4[mn.index(min(mn))]]
                    
                    rainLst[coordToProv[(x, y)]][0] += rgb2temp4[pxl]
                    rainLst[coordToProv[(x, y)]][1] += 1
    
    with Image.open('inundation.png') as img:
        for y in range(img.height):
            for x in range(img.width):
                pxl = img.getpixel((x, y))
                
                if pxl == 3:
                    inunLst[coordToProv[(x, y)]][0] += 1.5
                elif pxl == 2:
                    inunLst[coordToProv[(x, y)]][0] += 1.5
                elif pxl == 1:
                    inunLst[coordToProv[(x, y)]][0] += 1
                inunLst[coordToProv[(x, y)]][1] += 1
                    
    for i in soilLst:
        if i[1] > 0:
            soilLst[soilLst.index(i)] = i[0]/i[1]
        else:
            soilLst[soilLst.index(i)] = 0
    for i in heatAvgLst:
        if i[1] > 0:
            heatAvgLst[heatAvgLst.index(i)] = i[0]/i[1]
        else:
            heatAvgLst[heatAvgLst.index(i)] = 0
    for i in heatSeasonalLst:
        if i[1] > 0:
            heatSeasonalLst[heatSeasonalLst.index(i)] = i[0]/i[1]
        else:
            heatSeasonalLst[heatSeasonalLst.index(i)] = 0
    for i in heatDailyLst:
        if i[1] > 0:
            heatDailyLst[heatDailyLst.index(i)] = i[0]/i[1]
        else:
            heatDailyLst[heatDailyLst.index(i)] = 0
    for i in rainLst:
        if i[1] > 0:
            rainLst[rainLst.index(i)] = i[0]/i[1]
        else:
            rainLst[rainLst.index(i)] = 0
    for i in inunLst:
        if i[1] > 0:
            inunLst[inunLst.index(i)] = i[0]/i[1]
        else:
            inunLst[inunLst.index(i)] = 0
    
    if compute_from_map:
        import numpy as np
        colorprov = {rgb: prov for prov, rgb in provcolor.items()}
        provmap = np.array([colorprov[rgb] for rgb in mapimage.getdata()]).reshape((mapimage.height, mapimage.width))
        distortionmap = map_distortion(mapimage.height, mapimage.width)

            
    provinces = [p for p in range(1,provnumber) if (str(p) not in default_map["only_used_for_random"])]
    land_provinces = [p for p in provinces if (str(p) not in default_map["sea_starts"]) and
                        (str(p) not in default_map["lakes"])]
    positions_d = { prov:(float(positions[str(prov)]['position'][0]), float(positions[str(prov)]['position'][1]), 
                             float(positions[str(prov)]['position'][6]), float(positions[str(prov)]['position'][7]))
                       for prov in land_provinces }
    wasteland = [int(prov) for prov in climate['impassable']]
    sea_provinces = [p for p in provinces if (str(p) in default_map["sea_starts"] and (not str(p) in wasteland) and (str(p) not in default_map["lakes"]))]
    filtered_provs = [p for p in provinces if (str(p) not in climate['impassable']) and (str(p) not in default_map["lakes"])]

    s = ""
    text = comment
    latitude = longitude = 0
    stats=[]
    for i,prov in enumerate(filtered_provs): #or just land_provinces?
        if compute_from_map:
            provmask = provmap==prov
            size = distortionmap[provmask].sum()
            try:
                latitudes = provmask.sum(axis=1)
                latitude = float(np.average(np.arange(len(latitudes)), weights=latitudes))
                longitudes = provmask.sum(axis=0)
                longitude = float(np.average(np.arange(len(longitudes)), weights=longitudes))
            except ZeroDivisionError:
                latitude = longitude = 0
        else:
            try:
                color = provcolor[prov]
                size = colorsize[color]
                pos = positions[str(prov)]["position"]
                longitude = float(pos[0])
                latitude  = float(pos[1])
            except KeyError:
                size = 0
                latitude = longitude = 0
        
        coords = ""
        port = ""
        portdist = ""
        seazone = ""
        soil = ""
        heatAvg = ""
        heatSeasonal = ""
        heatDaily = ""
        rain = ""
        inun = ""
                
        prov_id = " set_key = { lhs = ID_Prov value =%4d }" % (prov)
        if prov in land_provinces:
            coords = " set_key = { lhs = Coord_X value = %.3f } set_key = { lhs = Coord_Y value = %.3f }" % (positions_d[prov][0], positions_d[prov][1])
            port = " set_key = { lhs = Coord_PortX value = %.3f } set_key = { lhs = Coord_PortY value = %.3f }" % (positions_d[prov][2], positions_d[prov][3])
            portdist = " set_key = { lhs = Land_PPort value = %.3f }" % math.sqrt((positions_d[prov][0] - positions_d[prov][2])**2 + (positions_d[prov][1] - positions_d[prov][3])**2)
            soil = ' set_key = { lhs = Land_Soil value = %.3f }' % soilLst[prov]
            heatAvg = ' set_key = { lhs = Land_AvgTemp value = %.3f }' % heatAvgLst[prov]
            heatSeasonal = ' set_key = { lhs = Land_SeasonalTemp value = %.3f }' % heatSeasonalLst[prov]
            heatDaily = ' set_key = { lhs = Land_DailyTemp value = %.3f }' % heatDailyLst[prov]
            rain = ' set_key = { lhs = Land_Rain value = %.3f }' % rainLst[prov]
            inun = ' set_key = { lhs = Land_Inundation value = %.3f }' % inunLst[prov]
        elif str(prov) in default_map["sea_starts"]:
            seazone = " set_key = { lhs = Coord_SeaX value = %.3f } set_key = { lhs = Coord_SeaY value = %.3f }" % (longitude, mapimage.height - latitude)
                        
        stats.append([prov, size, latitude, longitude])
        
        sizes  = " set_key = { lhs = Land_PSize value = %6d } set_key = { lhs = Land_PRad value = %.3f }" % (max(1, size), max(0.001, (size/3.1415)**0.5))
        
                            
        s += "\n\t\t%4d = {%s%s%s%s%s%s%s%s%s%s%s%s  }" % (prov, prov_id, coords, port, portdist, seazone, sizes, soil, heatAvg, heatSeasonal, heatDaily, rain, inun)

        if (i % prov_per_event == prov_per_event - 1) or i == len(filtered_provs)-1:
            eventid = int(i/prov_per_event) + 1
            if i<len(filtered_provs)-1:
                s += "\n\t\tcountry_event = { id = distance_calc.%d }" % ( eventid + 1 )
                
            text += event_structure % (eventid, s)
            s = ""

    add_provgroup(path, sea_provinces)

    
            
    return text, stats


north = 71.74        # northernmost latitude of the map
south = -58.7       # southernmost latitude of the map
equator = 1357 # pixelvalue of equator

def map_distortion(height, width):
    "trying to reconstruct Paradox's weird modified Miller projection"
    from numpy import arange, repeat, append, cos, tan, arctan, exp, log, pi
    def braun(phi):
        return 2. * tan(phi/2.)
    def braunReverse(y):
        return 2. * arctan(y/2.)
    
    scale = (braun(north / 180.*pi) - braun(south / 180.*pi)) / height
    y = (equator - arange(height)) * scale
    phi = braunReverse(y)
    distortion = cos(phi) * cos(phi)
    return repeat(distortion.reshape((1,-1)), width, axis=0).T

"""
def build_tree(path="", text={}):
    superregion = parse_file(os.path.join(path, "map", "superregion.txt"))
    region = parse_file(os.path.join(path, "map", "region.txt"))
    area = parse_file(os.path.join(path, "map", "area.txt"))
    tree = {}
    for sr in superregion.keys():
        s = []
        for re in superregion[sr]:
            for ar in region[re]["areas"]:
                s.append( (len(area[ar]), ar, re, ", ".join([repr(f) for f in text if ar in text[f]])) )
        tree[sr] = sorted(s,key=lambda i:i[0],reverse=True)
    return tree
    
def load_text(path=""):
    import glob
    text = {}
    files = glob.glob(os.path.join(path, "events", "*")) + glob.glob(os.path.join(path, "decisions", "*")) + glob.glob(os.path.join(path, "missions", "*"))
    for fn in files:
        with open(fn,"rb") as f:
            ff = f.read()
            text[fn] = ff.decode("iso-8859-1")
    return text
    
def show(tree):
    s = []
    for sr in tree:
        stat = [0.]*20
        ss = ""
        for ar in tree[sr]:
            stat[int(ar[0])]+=1
            ss += "\tProvs = %2d  %-20s %-20s Refs: %s\n" % ar
        mean = sum([stat[i]*i for i in range(20)])/sum(stat)
        s.append((mean,"Subcontinent = %s\tAvg. Prov/Area = %g\n" % (sr, mean) + ss))
    return "".join([ss[1]for ss in sorted(s,key=lambda i:i[0],reverse=True)])
"""

if __name__ == "__main__":
    import winsound
    path = ""
    with open(os.path.join(path,"events","00-Province_Setup.txt"),"w") as f:
        text, stats = province_stats(os.path.join(path, "map"), compute_from_map=True, prov_per_event=500)
        f.write(text)

    winsound.Beep(440, 500)
    winsound.Beep(440, 500)

    sys.stdout.write("Finished")
