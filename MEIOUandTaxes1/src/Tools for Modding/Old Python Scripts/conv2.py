if __name__ == '__main__':
    p1 = input()
    p2 = 'localisation\\00-locs_l_english.yml'

    with open(p2) as f:
        with open(p1) as ff:
            dct = dict()

            for line in f.readlines():
                [a, b] = line.split(':')
                dct[a.strip('\n\t ')] = b.strip('"\n\t[] ')
                
            t = ff.read()

            for key in dct:
                t = t.replace('[%s]' % key, '[%s]' % dct[key])

            with open(p1, 'w') as fff:
                fff.write(t)
            
