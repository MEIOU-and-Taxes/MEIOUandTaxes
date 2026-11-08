# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import codecs
import math

rights = pd.read_csv('RightsRaise.csv', index_col='Index', sep=';').dropna(how='all').replace({np.nan:None}).to_dict(orient='index')
rights_lower = pd.read_csv('RightsLower.csv', index_col='Index', sep=';').dropna(how='all').replace({np.nan:None}).to_dict(orient='index')
ui_matrix = pd.read_csv('RightsCrownlandButtonUI.csv', index_col='Index', sep=';').dropna(how='all').replace({np.nan:None}).to_dict(orient='index')

file6 = codecs.open('common/scripted_effects/SYS-RightsSteps.txt', 'w+', encoding='utf-8')
file7 = codecs.open('common/scripted_triggers/SYS-RightsSteps.txt', 'w+', encoding='utf-8')

loc_input = codecs.open('localisation/SYS-Rights_l_english.yml', 'r', encoding='utf-8-sig')

base_loc = loc_input.readlines()

def indent_block(text, depth = 1):
	out = ""
	for line in text.splitlines():
		line = line.strip()
		if not line:
			continue
		if line.startswith('}'):
			depth -= 1
		out += '\t' * depth + line + '\n'
		depth += line.count('{') - line.count('}') + (1 if line.startswith('}') else 0)
	return out

RightsSteps = ""
RightsStepTriggers = ""

for i in ui_matrix.keys():
	
	Type = ui_matrix[i]['Type']
	UD_Type = ui_matrix[i]['UD_Type']
	UD_Index = ui_matrix[i]['UD_Index']


	if Type == "Rights":
		Right = rights[UD_Index]['Right']
		Codename = rights[UD_Index]['Codename']
		Ranks = int(rights[UD_Index]['Ranks'])
		Interactions = int(rights[UD_Index]['Interactions'])
		DefaultPosition = int(rights[UD_Index]['DefaultPosition'])
		Mana_Ranks_Raise = rights[UD_Index]['Mana_Ranks'].split('|')
		Mana_Ranks_Lower = rights_lower[UD_Index]['Mana_Ranks'].split('|')
		
		effects_tmp = """if = {
			limit = {
				NOT = { stability = 1 }
				stability = -1
			}
        	custom_tooltip = Rights_LB
        	custom_tooltip = Rights_LowStab
			hidden_effect = {
				change_key = { lhs = NO_Mood value = -1 }
				change_key = { lhs = BG_Mood value = -1 }
				change_key = { lhs = CL_Mood value = -1 }
				change_key = { lhs = TR_Mood value = -1 }
			}
			custom_tooltip = NO_ReformMoodDispleased
			custom_tooltip = BG_ReformMoodDispleased
			custom_tooltip = CL_ReformMoodDispleased
			custom_tooltip = TR_ReformMoodDispleased
		}
		else_if = {
			limit = {
				NOT = { stability = -1 }
			}
        	custom_tooltip = Rights_LB
        	custom_tooltip = Rights_BadStab
			hidden_effect = {
				change_key = { lhs = NO_Mood value = -3 }
				change_key = { lhs = BG_Mood value = -3 }
				change_key = { lhs = CL_Mood value = -3 }
				change_key = { lhs = TR_Mood value = -3 }
			}
			custom_tooltip = NO_ReformMoodAngry
			custom_tooltip = BG_ReformMoodAngry
			custom_tooltip = CL_ReformMoodAngry
			custom_tooltip = TR_ReformMoodAngry
		}
		"""		
		index = 0
		for Rank in range(1,Ranks):
			CurRank = Rank + 1

			if UD_Type == "Raise":
				CodeRank = Rank + 1
				if(int(Mana_Ranks_Raise[index].split(',')[0]) != 0):
					Adm_Pow_Trig = 'adm_power = ' + Mana_Ranks_Raise[index].split(',')[0]
					Adm_Pow_Eff = 'add_adm_power = -' + Mana_Ranks_Raise[index].split(',')[0]
				else:
					Adm_Pow_Trig = ''
					Adm_Pow_Eff = ''
				if(int(Mana_Ranks_Raise[index].split(',')[1]) != 0):
					Dip_Pow_Trig = 'dip_power = ' + Mana_Ranks_Raise[index].split(',')[1]
					Dip_Pow_Eff = 'add_dip_power = -' + Mana_Ranks_Raise[index].split(',')[1]
				else:
					Dip_Pow_Trig = ''
					Dip_Pow_Eff = ''
				if(int(Mana_Ranks_Raise[index].split(',')[2]) != 0):
					Mil_Pow_Trig = 'mil_power = ' + Mana_Ranks_Raise[index].split(',')[2]
					Mil_Pow_Eff = 'add_mil_power = -' + Mana_Ranks_Raise[index].split(',')[2]
				else:
					Mil_Pow_Trig = ''
					Mil_Pow_Eff = ''
			else:
				CodeRank = Rank
				if(int(Mana_Ranks_Raise[index].split(',')[0]) != 0):
					Adm_Pow_Trig = 'adm_power = ' + Mana_Ranks_Lower[index].split(',')[0]
					Adm_Pow_Eff = 'add_adm_power = -' + Mana_Ranks_Lower[index].split(',')[0]
				else:
					Adm_Pow_Trig = ''
					Adm_Pow_Eff = ''
				if(int(Mana_Ranks_Raise[index].split(',')[1]) != 0):
					Dip_Pow_Trig = 'dip_power = ' + Mana_Ranks_Lower[index].split(',')[1]
					Dip_Pow_Eff = 'add_dip_power = -' + Mana_Ranks_Lower[index].split(',')[1]
				else:
					Dip_Pow_Trig = ''
					Dip_Pow_Eff = ''
				if(int(Mana_Ranks_Raise[index].split(',')[2]) != 0):
					Mil_Pow_Trig = 'mil_power = ' + Mana_Ranks_Lower[index].split(',')[2]
					Mil_Pow_Eff = 'add_mil_power = -' + Mana_Ranks_Lower[index].split(',')[2]
				else:
					Mil_Pow_Trig = ''
					Mil_Pow_Eff = ''

			index += 1


			if Rank == 1:
				step_trigger = """if = {{
	limit = {{ {Codename}{Rank}{Interaction_Type}Potential = yes }}
	{Adm_Pow}
	{Dip_Pow}
	{Mil_Pow}
	{Codename}{Rank}{Interaction_Type}Allow = yes
}}""".format(Codename=Codename, Rank = CodeRank, Interaction_Type = UD_Type, Adm_Pow = Adm_Pow_Trig, Dip_Pow = Dip_Pow_Trig, Mil_Pow = Mil_Pow_Trig)
				effects_tmp2 =	"""if = {{
	limit = {{ {Codename}{Rank}{Interaction_Type}Potential = yes }}
	custom_tooltip = Rights_LB
	custom_tooltip = {Codename}{Rank}{Interaction_Type}_description
	{Codename}{Rank}{Interaction_Type} = yes
	custom_tooltip = Rights_LB
	{Adm_Pow}
	{Dip_Pow}
	{Mil_Pow}
}}""".format(Codename=Codename, Rank = CodeRank, Interaction_Type = UD_Type,  Adm_Pow = Adm_Pow_Eff, Dip_Pow = Dip_Pow_Eff, Mil_Pow = Mil_Pow_Eff)
			else:
				step_trigger += """
else_if = {{
	limit = {{ {Codename}{Rank}{Interaction_Type}Potential = yes }}
	{Adm_Pow}
	{Dip_Pow}
	{Mil_Pow}
	{Codename}{Rank}{Interaction_Type}Allow = yes
}}""".format(Codename=Codename, Rank = CodeRank, Interaction_Type = UD_Type,  Adm_Pow = Adm_Pow_Trig, Dip_Pow = Dip_Pow_Trig, Mil_Pow = Mil_Pow_Trig)

				effects_tmp2 +=	"""
else_if = {{
	limit = {{ {Codename}{Rank}{Interaction_Type}Potential = yes }}
	custom_tooltip = Rights_LB
	custom_tooltip = {Codename}{Rank}{Interaction_Type}_description
	custom_tooltip = Rights_LB
	{Codename}{Rank}{Interaction_Type} = yes
	custom_tooltip = Rights_LB
	{Adm_Pow}
	{Dip_Pow}
	{Mil_Pow}
}}""".format(Codename=Codename, Rank = CodeRank, Interaction_Type = UD_Type,  Adm_Pow = Adm_Pow_Eff, Dip_Pow = Dip_Pow_Eff, Mil_Pow = Mil_Pow_Eff)


		step_trigger += """
else = {
	custom_trigger_tooltip = {
		tooltip = Rights_UI_NotAvail
		always = no
	}
}"""

		RightsSteps += "\n{Codename}{Interaction_Type}Step = {{\n{Body}}}\n".format(Codename=Codename, Interaction_Type = UD_Type, Body = indent_block(effects_tmp2 + "\n" + effects_tmp))
		RightsStepTriggers += "\n{Codename}{Interaction_Type}StepAllowed = {{\n{Body}}}\n".format(Codename=Codename, Interaction_Type = UD_Type, Body = indent_block(step_trigger))


file6.write("# One step up or down a rights ladder, with its costs and the estates' reaction (country scope)\n" + RightsSteps)
file7.write("""# Whether a rights ladder can take one step up or down now, costs included (country scope)

# The reform package is not too severe for another reform; $tooltip$ explains the limit
Rights_ReformSeverityOk = {
	custom_trigger_tooltip = {
		tooltip = $tooltip$
		NOT = { check_key = { lhs = Rights_SeverityR value = 10.001 } }
	}
}
""" + RightsStepTriggers)

file6.close
file7.close