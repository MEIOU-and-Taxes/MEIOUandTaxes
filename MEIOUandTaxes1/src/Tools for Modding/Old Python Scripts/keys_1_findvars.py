# by KJH & Phlopsi

import glob
import os

def remove_comment(block):
    while True:
        loc = block.find('#')

        if loc >= 0:
            comment = block[loc:]
            comment = comment[:comment.find('\n')]

            block = block[:loc] + block[loc + len(comment):]
        else:
            break

    return block

def parse_command(dct, command):
    command = command[command.find('{'):]

    if command.count('=') == 1:
        var = command[:command.find('=')].strip('{} \n\t')

        try:
            float(var)
        except:
            dct[var] = var
    else:
        command = command.replace('\n', ' ')
        command = command.replace('\t', ' ')
        command = command.replace('=', ' ')

        while '  ' in command:
            command = command.replace('  ', ' ')

        command = command.strip('{} ')
        command = command.split(' ')

        var = command[1]

        dct[var] = var

        var = command[3]

        try:
            float(var)
        except:
            dct[var] = var

def parse_paras(dct, command):
    command = command[command.find('{'):].strip('{} \n\t')

    command = command.replace('\n', ' ')
    command = command.replace('\t', ' ')
    command = command.replace('=', ' ')

    while '  ' in command:
        command = command.replace('  ', ' ')

    command = command.split(' ')

    for i in range(int(len(command)/2)):
        dct[command[2*i]] = command[2*i + 1]

def apply_meta(dct, name, paras):
    global meta

    for var in meta[name]:
        if type(meta[name][var]) == type(list()):
            for elem in meta[name][var]:
                newname = var

                if '$' in newname:
                    for para in paras:
                        newname = newname.replace('$%s$' % para, paras[para])

                newparas = dict(elem)
                
                for para in paras:
                    for paraa in newparas:
                        if newparas[paraa].strip('$') == para:
                            newparas[paraa] = paras[para]
                    
                apply_meta(dct, newname, newparas)
        else:
            for para in paras:
                var = var.replace('$%s$' % para, paras[para])

        dct[var] = var
        
def parse_block(block):
    global operators, dct, meta

    block = block[1:]

    while True:
        loc = block.find('{')

        if loc >= 0:
            name = block[:loc].rstrip(' \n\t=')

            loc1 = name.rfind(' ')
            loc2 = name.rfind('\t')
            loc3 = name.rfind('\n')

            if loc1 < loc2:
                loc1 = loc2
            if loc1 < loc3:
                loc1 = loc3

            name = name[loc1 + 1:]

            command = block[loc:]
            command = command[:command.find('}') + 1]

            if name in operators:
                parse_command(dct, command)
                
                block = block.replace(command, '', 1)
            elif name in meta:
                paras = dict()

                parse_paras(paras, command)
                
                apply_meta(dct, name, paras)
                
                block = block.replace(command, '', 1)
            else:
                block = block.replace('{', '', 1)
        else:
            break

def parse_effect(path):
    with open(path) as f:
        f = f.read()

        while True:
            loc = f.find('{')

            if loc >= 0:
                f = f[loc:]

                bracket = 0

                end = 1

                for char in f:
                    if char == '{':
                        bracket += 1
                    elif char == '}':
                        bracket -= 1

                    if not bracket:
                        break

                    end += 1

                block = remove_comment(f[:end])

                if not '$' in block:
                    parse_block(block)

                f = f[end + 1:]
            else:
                break

def parse_metascript(path):
    global meta
    
    with open(path) as f:
        f = f.read()

        while True:
            loc = f.find('{')

            if loc >= 0:
                name = f[:loc].rstrip(' =\n\t')
                
                loc1 = name.rfind(' ')
                loc2 = name.rfind('\t')
                loc3 = name.rfind('\n')

                if loc1 < loc2:
                    loc1 = loc2
                if loc1 < loc3:
                    loc1 = loc3

                name = name[loc1 + 1:]
                
                f = f[loc:]

                bracket = 0

                end = 1

                for char in f:
                    if char == '{':
                        bracket += 1
                    elif char == '}':
                        bracket -= 1

                    if not bracket:
                        break

                    end += 1

                block = remove_comment(f[:end])

                if '$' in block:
                    meta[name] = dict()

                f = f[end + 1:]
            else:
                break

def parse_meta(metaname, block):
    global meta
    
    block = block[1:]

    while True:
        loc = block.find('{')

        if loc >= 0:
            name = block[:loc].rstrip(' \n\t=')

            loc1 = name.rfind(' ')
            loc2 = name.rfind('\t')
            loc3 = name.rfind('\n')

            if loc1 < loc2:
                loc1 = loc2
            if loc1 < loc3:
                loc1 = loc3

            name = name[loc1 + 1:]

            command = block[loc:]
            command = command[:command.find('}') + 1]

            if name in operators:
                parse_command(meta[metaname], command)
                
                block = block.replace(command, '', 1)
            elif name in meta:
                if not name in meta[metaname]:
                    meta[metaname][name] = list()

                tmpdict = dict()
                    
                parse_paras(tmpdict, command)

                meta[metaname][name].append(tmpdict)
                
                block = block.replace(command, '', 1)
            else:
                block = block.replace('{', '', 1)
        else:
            break

def parse_metascript2(path):
    with open(path) as f:
        f = f.read()

        while True:
            loc = f.find('{')

            if loc >= 0:
                name = f[:loc].rstrip(' =\n\t')
                
                loc1 = name.rfind(' ')
                loc2 = name.rfind('\t')
                loc3 = name.rfind('\n')

                if loc1 < loc2:
                    loc1 = loc2
                if loc1 < loc3:
                    loc1 = loc3

                name = name[loc1 + 1:]
                
                f = f[loc:]

                bracket = 0

                end = 1

                for char in f:
                    if char == '{':
                        bracket += 1
                    elif char == '}':
                        bracket -= 1

                    if not bracket:
                        break

                    end += 1

                block = remove_comment(f[:end])

                if '$' in block:
                    parse_meta(name, block)

                f = f[end + 1:]
            else:
                break


def parse_event(path):
    global event_blocks
    
    with open(path) as f:
        f = f.read()

        for event_block in event_blocks:
            while True:
                loc = f.find(event_block)

                if loc >= 0:
                    block = f[loc:]

                    locc = block.find('{')
                    
                    block = block[locc:]

                    bracket = 0

                    end = 1

                    for char in block:
                        if char == '{':
                            bracket += 1
                        elif char == '}':
                            bracket -= 1

                        if not bracket:
                            break

                        end += 1

                    block = remove_comment(block[:end])

                    parse_block(block)

                    f = f[:loc] + f[loc + locc + end:]
                else:
                    break
            

operators = ['set_variable', 'change_variable', 'subtract_variable',
             'divide_variable', 'multiply_variable',
             'check_variable', 'is_variable_equal']
scopes = ['owner', 'ROOT', 'FROM', 'PREV', 'event_target:', 'THIS']
event_blocks = ['immediate', 'option', 'after']

dct = dict()
meta = dict()

effects = glob.glob(os.path.join('common', 'scripted_effects', '*.txt'))

for effect in effects:
    parse_metascript(effect)

for effect in effects:
    parse_metascript2(effect)

for effect in effects:
    parse_effect(effect)

events = glob.glob(os.path.join('events', '*.txt'))

for event in events:
    parse_event(event)

for i in dict(dct):
    try:
        float(i)

        dct.pop(i)
    except:
        if '$' in i:
            dct.pop(i)
        else:
            for scope in scopes:
                if scope in i:
                    dct.pop(i)

                    break

string = ''

for i in dct:
    string += i + '\n'

with open('vars.txt', 'w') as f:
    f.write(string)
