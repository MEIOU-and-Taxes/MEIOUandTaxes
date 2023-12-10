import glob
import os

# This file takes your LATEST savegame and extract all variables per province from it. 
# It also takes the variables stored in all history files per province.

# This script will produce a VariablesPerIDP file, which is likely to be between 100 to 200 mb in size. 
# Yes we got ALOT of provinces and ALOT of variables. 

# Dont be scared, this script takes between 4 to 20min, depending on your PC and the savegame. 
# The later it is ingame, the longer the extraction will take. 

# TODO: Merge both scripts together and store the endresult numpy array properly, instead of producing the VariablesPerIDP in between.   



def get_prov(idp, t):
    start = t.find('\n-%s={' % idp) + 1
    end = t[start:].find('\n\t}\n') + start + 3

    return t[start:end]

def get_var(t):
    if '\tvariables={' in t:
        start = t.find('\tvariables={') + len('\tvariables={')
        end = t[start:].find('}') + start

        return t[start:end].strip().replace('\t', '')
    else:
        return 'clz=0.000'

def get_history(prov, var):
    #out = '%s = {\n' % prov
    out = ''
    for v in var:
        v = v.split('=')
        if v[0] != 'and':
            if v[0] != 'not':
                if v[0] != 'for':
                    out += '%s' % v[0]
                    out += '[%s]' % prov
                    out += '=%s \n' % v[1]

    out += '\n'

    return out

def newest_save():
    saves = glob.glob(os.path.expanduser(os.path.join('~', 'Documents', 'Paradox Interactive', 'Europa Universalis IV', 'save games', '*')))
    return max(saves, key=os.path.getmtime)

with open(newest_save(), encoding='ISO-8859-1') as f:
    t = f.read()
    ttt = ''

    for prov in glob.glob(os.path.join('history', 'provinces', '*.txt')):
        with open(prov, encoding='ISO-8859-1') as ff:
            tt = ff.read()

            if '\n1.1.1' in tt:
                tt = tt[:tt.find('\n\n1.1.1')]
            
            idp = prov.split('\\')[-1].split('-')[0].strip()

            print(idp)

            block = get_prov(idp, t)

            var = get_var(block)

            if len(var) == 0:
                var = 'clz=0.000'

            var = var.split('\n')


            ttt += get_history(idp, var)

    event = '''%s''' % ttt

    with open(os.path.join('VariablesPerIDP.py'), 'w') as ff:
        ff.write(event)
