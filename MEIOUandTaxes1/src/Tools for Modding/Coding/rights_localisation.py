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
for key, value in dictionary['l_english'].items():
	if key.startswith('Rights_'):
		if (key.endswith('_desc') or key.endswith('_effects') or key.endswith('_t')) and not ('Lower_desc' in key or 'Raise_desc' in key or 'BackDown' in key or 'Reforms' in key):
			items[key] = value
		
keys_to_sub = {}
reforms = {}
for key in items.keys():
	if not re.findall(r'\d', key):
		key = key[:-2]
		reforms[key] = {}

for key in reforms.keys():
	for subkey,value in items.items():
		if key in subkey and '_t' in subkey and re.findall(r'\d', subkey):
			reforms[key][subkey[:-2]] = {}
	for subkey in reforms[key].keys():
		for subsubkey, value in items.items():
			if re.findall(r'{}\D'.format(subkey),subsubkey) and not '_t' in subkey:
				reforms[key][subkey][subsubkey] = value
	custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=key)
	for subkey in reforms[key].keys():
		level = int(re.findall(r'\d+',subkey)[0])
		lower = False
		upper = False
		current_level_key = subkey+'_t'
		current_level_desc_key = subkey+'_desc'
		custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=current_level_key)
		custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=current_level_desc_key)
		for subsubkey in reforms[key][subkey].keys():
			if 'Lower_effects' in subsubkey:
				lower = True
				next_level = level+1
				next_level_key = key+str(next_level)+'_t'
				current_level_lower_effects_key = subkey+'Lower_effects'
				custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=current_level_lower_effects_key)
			elif 'Raise_effects' in subsubkey:
				upper = True
				lower_level = level-1
				lower_level_key = key+str(lower_level)+'_t'
				current_level_raise_effects_key = subkey+'Raise_effects'
				custom_loc_total += """\ndefined_text = {{
	name = {NAME}
	text = {{
		localisation_key = {NAME}
		triggers = {{
			always = yes
		}}
	}}				
}}""".format(NAME=current_level_raise_effects_key)
		if lower:
			keys_to_sub[subkey+'Lower_desc'] = r"""Transition from [{}] to [{}]\\n[{}]\\n[{}]\\n[{}]""".format(next_level_key,current_level_key,key,current_level_desc_key,current_level_lower_effects_key)
			lower = False
		if upper:
			keys_to_sub[subkey+'Raise_desc'] = r"""Transition from [{}] to [{}]\\n[{}]\\n[{}]\\n[{}]""".format(lower_level_key,current_level_key,key,current_level_desc_key,current_level_raise_effects_key)
			upper = False


with open('SYS-Rights_l_english.yml','r',encoding='utf-8') as file:
	contents = file.read()

for key,value in keys_to_sub.items():
	contents = re.sub(r'{}.*'.format(key), """{}: \"{}\"""".format(key,value),contents)
	
with open('SYS-Rights_l_english.yml','w',encoding='utf-8') as file:
	file.write(contents)	
	
custom_loc_file.write(custom_loc_total)

custom_loc_file.close()