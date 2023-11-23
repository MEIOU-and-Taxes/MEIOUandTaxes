import glob
import os

def get_prov(idp, t):
    start = t.find('\n-%s={' % idp) + 1
    end = t[start:].find('\n\t}\n') + start + 3

    return t[start:end]

def get_country(tag, t):
    start = t.find('\t}\n\t%s={\n' % tag)
    end = t[start:].find('\n\t}\n') + start

    return t[start:end]

def get_var(t):
    if '\tvariables={' in t:
        start = t.find('\tvariables={') + len('\tvariables={')
        end = t[start:].find('}') + start

        return t[start:end].strip().replace('\t', '')
    else:
        return 'clz=0.000'

def get_flag(t):
    if '\tflags={' in t:
        start = t.find('\tflags={') + len('\tflags={')
        end = t[start:].find('}') + start

        return t[start:end].strip().replace('\t', '')
    else:
        return 'foo=1356.1.1'

def get_modifier(t):
    out = []
    
    while '\t\tmodifier={' in t:
        start = t.find('\t\tmodifier={')
        end = t[start:].find('}') + start + 1

        block = t[start:end]
        
        if '\tpermanent=yes\n' in block:
            tstr = '_ppm'
        else:
            tstr = '_pm'

        if '\thidden=yes\n' in block:
            tstr += 'h'

        tstr += '={m=%s}' % block[block.find('"') + 1:block.find('"\n')]

        out.append(tstr)

        t = t[:start] + t[end + 1:]

    return out

def get_modifier2(t):
    out = []
    
    while '\t\tmodifier={' in t:
        start = t.find('\t\tmodifier={')
        end = t[start:].find('}') + start + 1

        block = t[start:end]

        if '\thidden=yes\n' in block:
            tstr = '_cmh'
        else:
            tstr = '_cm'

        tstr += '={m=%s}' % block[block.find('"') + 1:block.find('"\n')]

        out.append(tstr)

        t = t[:start] + t[end + 1:]

    return out

def get_history(prov, var, flag, modifier):
    out = '%s = {\n' % prov

    for v in var:
        v = v.split('=')
        if v[1] != '0.000':
            out += '_v={v=%s n=%s} ' % (v[0], v[1])

    out += '\n'
    
    for f in flag:
        if len(f) > 0:
            out += '_pf={f=%s} ' % f

    out += '\n'

    for m in modifier:
        out += '%s ' % m

    out += '}\n'

    return out

def get_history2(tag, var, flag, modifier):
    out = '%s = {\n' % tag

    for v in var:
        v = v.split('=')
        
        if v[1] != '0.000':
            out += '_v={v=%s n=%s} ' % (v[0], v[1])

    out += '\n'
    
    for f in flag:
        if len(f) > 0:
            out += '_cf={f=%s} ' % f

    out += '\n'

    for m in modifier:
        out += '%s ' % m

    out += '}\n'

    return out

def newest_save():
    saves = glob.glob(os.path.expanduser(os.path.join('~', 'Documents', 'Paradox Interactive', 'Europa Universalis IV', 'save games', '*')))
    return max(saves, key=os.path.getmtime)

with open(newest_save(), encoding='ISO-8859-1') as f:
    t = f.read()
    ttt = 'immediate = {\n'

    for prov in glob.glob(os.path.join('history', 'provinces', '*.txt')):
        with open(prov, encoding='ISO-8859-1') as ff:
            tt = ff.read()

            if '\n1.1.1' in tt:
                tt = tt[:tt.find('\n\n1.1.1')]
            
            idp = prov.split('\\')[-1].split('-')[0].strip()

            print(idp)

            block = get_prov(idp, t)

            var = get_var(block)
            flag = get_flag(block)
            modifier = get_modifier(block)

            if len(var) == 0:
                var = 'clz=0.000'

            flag = flag.split('\n')
            var = var.split('\n')

            for ind, ff in enumerate(flag):
                flag[ind] = ff.split('=')[0]

            ttt += get_history(idp, var, flag, modifier)

    for country in glob.glob(os.path.join('history', 'countries', '*.txt')):
        with open(country, encoding='ISO-8859-1') as ff:
            tt = ff.read()

            if '\n1.1.1' in tt:
                tt = tt[:tt.find('\n\n1.1.1')]
            
            tag = country.split('\\')[-1].split('-')[0].strip()

            print(tag)

            block = get_country(tag, t)

            var = get_var(block)
            flag = get_flag(block)
            modifier = get_modifier2(block)

            if len(var) == 0:
                var = 'clz=0.000'

            flag = flag.split('\n')
            var = var.split('\n')
            
            for ind, ff in enumerate(flag):
                flag[ind] = ff.split('=')[0]

            ttt += get_history2(tag, var, flag, modifier)

    ttt += '}'

    event = '''namespace = POP_Init
country_event = {
    id = POP_Init.001
    title = no_localisation
    desc = no_localisation
    picture = MEIOU_AND_TAXES_eventPicture
    is_triggered_only = yes
    %s
    option = {
    }
}''' % ttt

    with open(os.path.join('events', '00-POP_Init.txt'), 'w') as ff:
        ff.write(event)
