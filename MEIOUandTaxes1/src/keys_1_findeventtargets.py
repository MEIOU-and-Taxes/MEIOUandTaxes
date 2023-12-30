
import glob
import os

os.chdir(os.path.dirname(__file__))

dont = ['keys.txt', '00-scripts.txt', '00-triggers.txt',
        'vars.txt', '00-locs_l_english.yml', '00-locs.txt']

with open('event_targets.txt', 'r') as file:
    scopesset = {scope.strip('\n') for scope in file.readlines()}

    for path in glob.glob(os.path.join('**', '*.txt'), recursive = True):
        do = True

        for dontt in dont:
            if dontt in path:
                do = False

                break

        if do:
            with open(path, encoding='ISO-8859-1') as f:
                for line in f.readlines():
                    if 'event_target:' in line:
                        line = line[line.find('event_target:') + 13:]
                        line = line.replace('\n', ' ')
                        line = line.replace('\t', ' ')
                        line = line.replace('}', ' ')
                        line = line.replace(']', ' ')
                        line = line[:line.find(' ')]
                        
                        scopesset.add(line)
    
    scopes = list(scopesset)
    scopes.sort()

with open('event_targets.txt', 'w') as file:
    for scope in scopes:
        file.write(scope + '\n')