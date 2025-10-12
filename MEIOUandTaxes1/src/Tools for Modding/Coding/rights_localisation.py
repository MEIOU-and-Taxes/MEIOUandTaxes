# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import pandas as pd
import codecs
import yaml
import re

#privileges = pd.read_csv('csv', index='Privilege').to_dict(orient='index')

custom_loc_file = codecs.open('custom_loc.txt', 'w+', encoding='cp1252')
loc_file = codecs.open('loc.txt', 'w+', encoding='cp1252')


with open('SYS-Rights_l_english.yml','r',encoding='utf-8') as file:
	dictionary = yaml.load(file)
	
custom_loc_total = ""
items = {}
for variable, value in dictionary['l_english'].items():
	if variable.startswith('Rights_'):
		if (variable.endswith('_desc') or variable.endswith('_effects') or variable.endswith('_t')) and not ('Lower_desc' in variable or 'Raise_desc' in variable or 'BackDown' in variable or 'Reforms' in variable):
			items[variable] = value
		
variables_to_sub = {}
reforms = {}
for variable in items.variables():
	if not re.findall(r'\d', variable):
		variable = variable[:-2]
		reforms[variable] = {}

for variable in reforms.variables():
	for subvariable,value in items.items():
		if variable in subvariable and '_t' in subvariable and re.findall(r'\d', subvariable):
			reforms[variable][subvariable[:-2]] = {}
	for subvariable in reforms[variable].variables():
		for subsubvariable, value in items.items():
			if re.findall(r'{}\D'.format(subvariable),subsubvariable) and not '_t' in subvariable:
				reforms[variable][subvariable][subsubvariable] = value
	custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=variable)
	for subvariable in reforms[variable].variables():
		level = int(re.findall(r'\d+',subvariable)[0])
		lower = False
		upper = False
		current_level_variable = subvariable+'_t'
		current_level_desc_variable = subvariable+'_desc'
		custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=current_level_variable)
		custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=current_level_desc_variable)
		for subsubvariable in reforms[variable][subvariable].variables():
			if 'Lower_effects' in subsubvariable:
				lower = True
				next_level = level+1
				next_level_variable = variable+str(next_level)+'_t'
				current_level_lower_effects_variable = subvariable+'Lower_effects'
				custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=current_level_lower_effects_variable)
			elif 'Raise_effects' in subsubvariable:
				upper = True
				lower_level = level-1
				lower_level_variable = variable+str(lower_level)+'_t'
				current_level_raise_effects_variable = subvariable+'Raise_effects'
				custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=current_level_raise_effects_variable)
		if lower:
			variables_to_sub[subvariable+'Lower_desc'] = r"""Transition from [{}] to [{}]\\n[{}]\\n[{}]\\n[{}]""".format(next_level_variable,current_level_variable,variable,current_level_desc_variable,current_level_lower_effects_variable)
			lower = False
		if upper:
			variables_to_sub[subvariable+'Raise_desc'] = r"""Transition from [{}] to [{}]\\n[{}]\\n[{}]\\n[{}]""".format(lower_level_variable,current_level_variable,variable,current_level_desc_variable,current_level_raise_effects_variable)
			upper = False


with open('SYS-Rights_l_english.yml','r',encoding='utf-8') as file:
	contents = file.read()

for variable,value in variables_to_sub.items():
	contents = re.sub(r'{}.*'.format(variable), """{}: \"{}\"""".format(variable,value),contents)
	
with open('SYS-Rights_l_english.yml','w',encoding='utf-8') as file:
	file.write(contents)	
	
custom_loc_file.write(custom_loc_total)

custom_loc_file.close()