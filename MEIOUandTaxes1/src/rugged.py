from PIL import Image
import numpy as np
import scipy.stats
from provsize import parse_file
import sys
import os

if __name__ == '__main__':
    imgs = dict()
    arrs = dict()

    default_map = parse_file('map/default.map')

    provcolor = dict()
    
    with open('map/definition.csv', 'rb') as f:
        for line in f.readlines()[1:]:
            l = line.decode("latin-1").split(';')
            provcolor[(int(l[1]), int(l[2]), int(l[3]))] = int(l[0])

    climate = parse_file("map/climate.txt")
    provnumber = int(default_map["max_provinces"])
    provinces = [p for p in range(1,provnumber) if (str(p) not in default_map["only_used_for_random"])]
    land_provinces = set(p for p in provinces if (str(p) not in default_map["sea_starts"]) and
                        (str(p) not in default_map["lakes"]) and (str(p) not in climate['impassable']))
    
    imgs['prov'] = Image.open('map/provinces.bmp')
    imgs['height'] = Image.open('heightmap.bmp')
    arrs['prov'] = np.array(imgs['prov'], dtype='int16')
    arrs['height'] = np.array(imgs['height'], dtype='int16')

    if not os.path.exists('sea.bmp'):
        t = np.zeros(arrs['prov'].shape[:-1], dtype='bool')
        tt = set([color for color, prov in provcolor.items() if prov in default_map['sea_starts'] or prov in default_map['lakes']])

        for i in range(t.shape[0]):
            for ii in range(t.shape[1]):
                if tuple(arrs['prov'][i][ii]) in tt:
                    t[i][ii] = True

        Image.fromarray(np.uint8(tt) * 255, 'L').save('sea.bmp')

        arrs['sea'] = tt
    else:
        t = Image.open('sea.bmp')
        t = np.array(t, dtype='bool')

        arrs['sea'] = t
        
    t = [(s, a) for a in [0, 1, (0, 1)] for s in [-1, 1]] + [((-1, 1), (0, 1)), ((1, -1), (0, 1))]
    t = [np.roll(arrs['height'], tt[0], tt[1]) for tt in t]
    t = [np.abs(arrs['height'] - tt) for tt in t]
    t = np.array(t, dtype='float32')
    #t *= np.log(t + 10)
    t *= np.sqrt(t)
    t[4:,:,:] *= np.sqrt(2)
    t = np.sum(t, 0)
    tt = np.max(t)
    t /= tt / 255
    t = np.array([t, arrs['height']], dtype='float32')
    t = scipy.stats.hmean(t, 0)
    tt = np.max(t) * 0.5
    t[t > tt] = tt
    t /= tt / 255

    imgs['rugged'] = Image.fromarray(np.uint8(t), 'L')
    arrs['rugged'] = t
    
    rugged = dict()

    for y in range(arrs['prov'].shape[0]):
        for x in range(arrs['prov'].shape[1]):
            if not arrs['sea'][y][x]:
                t = tuple(arrs['prov'][y][x])
                t = provcolor[t]

                if t in rugged:
                    rugged[t][0] += arrs['rugged'][y][x]
                    rugged[t][1] += 1
                else:
                    rugged[t] = [arrs['rugged'][y][x], 1]

    eff = list()

    for prov in land_provinces:
        if prov in rugged:
            eff.append('%s = { set_key = { lhs = Land_Rugged value = %.3f } }' % (prov, min(100, rugged[prov][0] / rugged[prov][1] / 255 * 100)))
        else:
            eff.append('%s = { set_key = { lhs = Land_Rugged value = 1 } }' % prov)

    with open('out.txt', 'w') as f:
        f.write('\n'.join(eff))

    imgs['rugged'].save('out.bmp')
