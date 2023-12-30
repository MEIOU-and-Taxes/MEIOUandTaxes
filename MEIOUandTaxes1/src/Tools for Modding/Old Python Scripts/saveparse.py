import glob

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
            tstr = 'add_permanent_province_modifier = { '
        else:
            tstr = 'add_province_modifier = { '

        tstr += 'name = %s duration = -1 ' % block[block.find('"') + 1:block.find('"\n')]

        if '\thidden=yes\n' in block:
            tstr += 'hidden = yes '

        tstr += '}'

        out.append(tstr)

        t = t[:start] + t[end + 1:]

    return out

def get_modifier2(t):
    out = []
    
    while '\t\tmodifier={' in t:
        start = t.find('\t\tmodifier={')
        end = t[start:].find('}') + start + 1

        block = t[start:end]
        
        tstr = 'add_country_modifier = { name = %s duration = -1 ' % block[block.find('"') + 1:block.find('"\n')]

        if '\thidden=yes\n' in block:
            tstr += 'hidden = yes '

        tstr += '}'

        out.append(tstr)

        t = t[:start] + t[end + 1:]

    return out

def get_history(var, flag, modifier):
    out = '1.1.1 = {\n'

    for v in var:
        v = v.split('=')
        
        out += '\tset_variable = { which = %s value = %s }\n' % (v[0], v[1])
    
    for f in flag:
        out += '\tset_province_flag = %s\n' % f

    for m in modifier:
        out += '\t%s\n' % m

    out += '}'

    return out

def get_history2(var, flag, modifier):
    out = '1.1.1 = {\n'

    for v in var:
        v = v.split('=')

        out += '\tset_variable = { which = %s value = %s }\n' % (v[0], v[1])
    
    for f in flag:
        out += '\tset_country_flag = %s\n' % f

    for m in modifier:
        out += '\t%s\n' % m

    out += '}'

    return out

with open('inp.eu4', encoding='ISO-8859-1') as f:
    t = f.read()

    for prov in glob.glob('history\provinces\*.txt'):
        with open(prov, encoding='ISO-8859-1') as ff:
            tt = ff.read()

            if '\n1.1.1' in tt:
                tt = tt[:tt.find('\n\n1.1.1')]
            
            idp = prov.split('\\')[-1].split('-')[0].strip()

            block = get_prov(idp, t)

            var = get_var(block)
            flag = get_flag(block)
            modifier = get_modifier(block)

            var = var.split('\n')
            flag = flag.split('\n')

            for ind, ff in enumerate(flag):
                flag[ind] = ff.split('=')[0]

            tt += '\n\n' + get_history(var, flag, modifier)

            with open(prov, 'w', encoding='ISO-8859-1') as fff:
                fff.write(tt)

    for country in glob.glob('history\countries\*.txt'):
        with open(country, encoding='ISO-8859-1') as ff:
            tt = ff.read()

            if '\n1.1.1' in tt:
                tt = tt[:tt.find('\n\n1.1.1')]
            
            tag = country.split('\\')[-1].split('-')[0].strip()

            block = get_country(tag, t)

            var = get_var(block)
            flag = get_flag(block)
            modifier = get_modifier2(block)

            if len(var) == 0:
                var = 'clz=0.000'
            
            var = var.split('\n')
            flag = flag.split('\n')
            
            for ind, ff in enumerate(flag):
                flag[ind] = ff.split('=')[0]

            tt += '\n\n' + get_history2(var, flag, modifier)

            with open(country, 'w', encoding='ISO-8859-1') as fff:
                fff.write(tt)
