# by KJH & Phlopsi

import glob
import os

os.chdir(os.path.dirname(__file__))

def check_error(command):
    command = command[command.find('{') + 1:]
    command = command[:command.find('}')]

    command = command.replace('\n', ' ')
    command = command.replace('\t', ' ')
    command = command.replace('=', ' ')

    while '  ' in command:
        command = command.replace('  ', ' ')

    command = command.strip(' ').split(' ')
    command = [i.strip(' ') for i in command]

    if len(command) != 4:
        return True
    if command[0] != 'lhs':
        return True
    if command[1] == 'lhs' or command[1] == 'which' or command[1] == 'value' or command[1] == 'PREV' or command[1] == 'ROOT' or 'event_target:' in command[1]:
        return True
    if command[2] != 'which' and command[2] != 'value' and not '$' in command[2]:
        return True
    if command[2] == 'value' and not '$' in command[3]:
        try:
            float(command[3])
        except:
            return True
    if command[3] == 'lhs' or command[3] == 'which' or command[3] == 'value':
        return True

    return False

def update_script(path):
    with open(path, encoding='ISO-8859-1') as f:
        effect = f.read()

        for operator in operators:
            last = 0

            while operator in effect[last:]:
                command = effect[last:]
                command = command[command.find(operator):]
                command = command[:command.find('}') + 1]

                command_save = str(command)

                while '#' in command:
                    comment = command[command.find('#'):]
                    comment = comment[:comment.find('\n')]

                    command = command.replace(comment, '', 1)
                
                command = command[command.find('=') + 1:].strip('\n\t {}')

                command = command.replace('\n', ' ')
                command = command.replace('\t', ' ')
                command = command.replace('=', ' = ')
                command = command.replace('"', '')

                while '  ' in command:
                    command = command.replace('  ', ' ')

                newoperator = operator.replace('variable', 'key')

                if len(command) > 0:
                    if command.count('=') == 1:
                        command = command.split('=')

                        command = '%s = { lhs = %s value = %s }' % (newoperator, command[0].strip(' \n\t'), command[1].strip(' \n\t'))
                    else:
                        command = command.split(' ')
                        
                        command = '%s = { lhs = %s %s = %s }' % (newoperator, command[2], command[3], command[5])

                    if check_error(command):
                        print(command)
                        
                    effect = effect.replace(command_save, command + '%s', 1)

                    last = effect.find('%s')

                    effect = effect.replace('%s', '')
                else:
                    last += len(command_save)

        with open(path, 'w', encoding='ISO-8859-1') as ff:
            ff.write(effect)

def update_local(dct, path):
    with open(path, encoding='ISO-8859-1') as f:
        local = f.read()
        
        for var in dct:
            if var in local:
                local = local.replace('Root.%s.GetValue' % var, 'GV_%s' % var)

        with open(path, 'w', encoding='ISO-8859-1') as ff:
            ff.write(local)

with open('keys.txt') as f:
    dct = dict()

    for line in f.readlines():
        line = line.split(':')

        dct[line[0].strip('\n\t ')] = line[1].strip('\n\t ')

operators = ['set_variable', 'change_variable', 'subtract_variable',
             'divide_variable', 'multiply_variable',
             'check_variable', 'is_variable_equal']
dont = ['keys.txt', '00-scripts.txt', '00-triggers.txt',
        'vars.txt', '00-locs_l_english.yml', '00-locs.txt']
for path in glob.glob(os.path.join('**', '*.txt'), recursive = True):
    in_dont = False

    for dontt in dont:
        if dontt in path:
            in_dont = True

            break
        
    if not in_dont:
        update_script(path)

for path in glob.glob(os.path.join('**', '*.yml'), recursive = True):
    in_dont = False

    for dontt in dont:
        if dontt in path:
            in_dont = True

            break
        
    if not in_dont:
        update_local(dct, path)
