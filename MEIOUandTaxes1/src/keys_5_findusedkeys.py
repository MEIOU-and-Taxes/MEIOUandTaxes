# by KJH & Phlopsi

import glob
import os

variableList = dict()
variableListT = dict()

def check_script(path):
    with open(path, 'r', encoding='ISO-8859-1') as f:
        content = f.read()
        for variable, var in variableList.items():
            if variable in content:
                variableList[variable] = True
    

def check_dont(path, dont):
	for item in dont:
		if item in path:
			return True
		
	return False

def pathcont (text):
	return os.path.join('', text, '')

def pathstart (text):
	return os.path.join(text, '')

def pathend (text):
	return os.path.join('', text)

dont = ['Tools for Modding', 'graphicalculturetype.txt', pathcont('bookmarks'), pathcont('countries'), pathcont('country_colors'), pathcont('country_tags'),
    pathcont('cultures'), pathcont('event_modifiers'), pathcont('opinion_modifiers'), pathstart('map'), pathstart('interface'), pathstart('gfx'), pathcont('units'),
    pathcont('static_modifiers'), pathcont('countries'), pathcont('country_tags'), pathcont('province_names'), pathcont('tradenodes'), 'SYS-CensusDisplay.txt',
    pathcont('event_modifiers'), pathcont('scripted_effects'), pathcont('scripted_triggers'), 'keys.txt', '00-scripts_core.txt', '00-scripts.txt', '00-triggers_core.txt', '00-triggers.txt',
        'vars.txt', '00-locs_l_english.yml', '00-locs.txt', 
    '00-POP_Init.txt', '00-POP_Init-0.txt', '00-POP_Init-1.txt', '00-POP_Init-2.txt']


with open("keys.txt", encoding='ISO-8859-1') as f:
    for l_no, line in enumerate(f):
        variableset = line.split(':')
        variableList[variableset[1].strip('\n\t ')] = False
        variableListT[variableset[1].strip('\n\t ')] = variableset[0].strip('\n\t ')
paths = [path for path in glob.glob(os.path.join('*', '**', '*.txt'), recursive=True) if not check_dont(path, dont)]
for path in paths:
    print(path)
    print(len(variableList))
    check_script(path)
    variableList = {k: v for k, v in variableList.items() if not v}

for variable, var in variableList.items():
    variableListT.pop(variable)

with open("newVars.txt", 'w', encoding='ISO-8859-1') as f:
    for variable, var in variableListT.items():
        f.write("%s\n" % var)