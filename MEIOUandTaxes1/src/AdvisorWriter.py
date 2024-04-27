# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import codecs
import math

advisors = pd.read_csv('advisors.csv', index_col='Index', sep=';').dropna(how='all').replace({pd.np.nan:None}).to_dict(orient='index')

file = codecs.open('common/advisortypes/00_BG_advisors.txt', 'w+', encoding='utf-8')
file1 = codecs.open('common/advisortypes/00_NO_advisors.txt', 'w+', encoding='utf-8')
file2 = codecs.open('common/advisortypes/00_CL_advisors.txt', 'w+', encoding='utf-8')
file3 = codecs.open('common/advisortypes/00_BU_advisors.txt', 'w+', encoding='utf-8')
file4 = codecs.open('common/advisortypes/00_TR_advisors.txt', 'w+', encoding='utf-8')
file5 = codecs.open('localisation/SYS-Advisors_l_english.yml', 'w+', encoding='utf-8-sig')
file6 = codecs.open('common/scripted_triggers/SYS-Advisors_Misc.txt', 'w+', encoding='utf-8')
file7 = codecs.open('AdvisorsScriptedEffect.txt', 'w+', encoding='utf-8')
loc_input = codecs.open('localisation/replace/text_l_english.yml', 'r', encoding='utf-8-sig')

base_loc = loc_input.readlines()

AdvisorsBU = ""
AdvisorsBG = ""
AdvisorsCL = ""
AdvisorsNO = ""
AdvisorsTR = ""
AdvisorsL = """l_english:
"""
AdvisorTmp = ""
AdvisorTrigger = ""
tmp2 = ""
for key in advisors.keys():
	
	Codename = advisors[key]['Codename']
	Manatype = advisors[key]['Manatype']
	Modifier1 = advisors[key]['Modifier1']
	Modifier2 = advisors[key]['Modifier2']
	Modifier3 = advisors[key]['Modifier3']
	Factions = advisors[key]['Factions'].split(' ')
	Factor1 = advisors[key]['Factor1']
	Factor2 = advisors[key]['Factor2']
	Factor3 = advisors[key]['Factor3']
	
	if(Modifier1 == None):
		Modifier1 = ''
	if(Modifier2 == None):
		Modifier2 = ''
	if(Modifier3 == None):
		Modifier3 = ''
	if(Factor1 == None):
		Factor1 = ''
	if(Factor2 == None):
		Factor2 = ''
	if(Factor3 == None):
		Factor3 = ''

	AdvisorTrigger += """{Codename} = {{
	OR = {{
""".format(Codename=Codename)

	for Faction in Factions:

		AdvisorTmp = """{Codename}_{Faction} = {{
	monarch_power = {Manatype}
	{Modifier1}
	{Modifier2}
	{Modifier3}

	skill_scaled_modifier = {{ modifier = {{ yearly_corruption = 0.05 }} }}
	skill_scaled_modifier = {{ modifier = {{ FC_{Faction}_influence = 0.05 }} }}
	
	chance = {{
		factor = 1
		modifier = {{
			factor = 0.25
			owner = {{ {Codename}_{Faction} = 1 }}
		}}
		modifier = {{
			factor = 0.1
			owner = {{ NOT = {{ has_faction = FC_{Faction} }} }}
		}}
		modifier = {{
			factor = 0.95
			owner = {{ NOT = {{ check_key = {{ lhs = Prov_{Faction}Pow value = 80 }} }} }}
		}}
		modifier = {{
			factor = 0.95
			owner = {{ NOT = {{ check_key = {{ lhs = Prov_{Faction}Pow value = 60 }} }} }}
		}}
		modifier = {{
			factor = 0.95
			owner = {{ NOT = {{ check_key = {{ lhs = Prov_{Faction}Pow value = 40 }} }} }}
		}}
		modifier = {{
			factor = 0.95
			owner = {{ NOT = {{ check_key = {{ lhs = Prov_{Faction}Pow value = 20 }} }} }}
		}}
		modifier = {{
			factor = 0
			AND = {{ 
				owner = {{ NOT = {{ check_key = {{ lhs = Prov_{Faction}Pow value = 1.0 }} }} }}
				is_year = 1357
			}}
		}}
		{Factor1}
		{Factor2}
		{Factor3}
	}}
	
	ai_will_do = {{
		factor = 1
	}}
}}
""".format(Codename=Codename,Faction=Faction, Manatype=Manatype, Modifier1=Modifier1, Modifier2=Modifier2, Modifier3=Modifier3, Factor1=Factor1.replace('     ','\n'), Factor2=Factor2.replace('     ','\n'), Factor3=Factor3.replace('      ','\n'))
		if(Faction == 'BG'):
			AdvisorsBG += AdvisorTmp
		elif(Faction == 'NO'):
			AdvisorsNO += AdvisorTmp
		elif(Faction == 'TR'):
			AdvisorsTR += AdvisorTmp
		elif(Faction == 'CL'):
			AdvisorsCL += AdvisorTmp
		elif(Faction == 'BU'):
			AdvisorsBU += AdvisorTmp

		AdvisorTrigger += """		{Codename}_{Faction} = $Level$
""".format(Codename=Codename,Faction=Faction)
		i = 0
		index_title = -1
		index_desc = -1
		SearchTitle = ' ' + Codename + '_' + Faction
		SearchDesc = ' ' + Codename + '_' + Faction + '_desc'
		for loc in base_loc:
			try:
				if loc.split(':')[0] == SearchTitle or loc.split(':')[0] == ' ' + Codename:
					index_title = i
			except Exception:
				pass  # or you could use 'continue'
			
			try:
				if loc.split(':')[0] == SearchDesc or loc.split(':')[0] == ' ' + Codename + '_desc':
					index_desc = i
			except Exception:
				pass  # or you could use 'continue'
			i += 1

		if index_title != -1:
			GenTitle = base_loc[index_title].replace('\n', '').replace('\r', '')
			GenTitle = GenTitle.split(':')[1]
			GenTitle = GenTitle.split('"')[1] + GenTitle.split('"')[2]
		if index_desc != -1:
			GenDesc = base_loc[index_desc].replace('\n', '').replace('\r', '')
			GenDesc = GenDesc.split(':')[1]
			GenDesc = GenDesc.split('"')[1] + GenDesc.split('"')[2]

		if(Faction == 'BG'):
			FactionIcon = "£estate_city_burghers_icon_small£"
		elif(Faction == 'NO'):
			FactionIcon = "£estate_greater_nobles_icon_small£"
		elif(Faction == 'TR'):
			FactionIcon = "£estate_nomadic_tribes_icon_small£"
		elif(Faction == 'CL'):
			FactionIcon = "£estate_church_icon_small£"
		elif(Faction == 'BU'):
			FactionIcon = "£estate_bureaucracy_icon_small£"

		AdvisorsL += """ {Codename}_{Faction}:2 "{gen_title} ({FactionIcon} Faction)"
 {Codename}_{Faction}_desc:2 "{gen_desc}"
""".format(Codename=Codename, Faction=Faction,  FactionIcon = FactionIcon, gen_title = GenTitle, gen_desc = GenDesc)
		if(Faction == 'BG'):
			FactionValue = 2
		elif(Faction == 'NO'):
			FactionValue = 1
		elif(Faction == 'TR'):
			FactionValue = 4
		elif(Faction == 'CL'):
			FactionValue = 3
		elif(Faction == 'BU'):
			FactionValue = 5
		
		tmp2 += """			{Codename}_{Faction} = {{
				if = {{
					limit = {{
						{Codename}_{Faction} = 3
					}}
					set_key = {{ lhs = Advisor_{Manatype} value = 3 }}
				}}
				else_if = {{
					limit = {{
						{Codename}_{Faction} = 2
					}}
					set_key = {{ lhs = Advisor_{Manatype} value = 2 }}
				}}
				else = {{
					set_key = {{ lhs = Advisor_{Manatype} value = 1 }}
				}}
				#set_key = {{ lhs = Advisor_{Manatype}Type value = 1 }}
				set_key = {{ lhs = Advisor_{Manatype}Faction value = {FactionValue} }}
			}}
""".format(Codename=Codename, Manatype=Manatype, Faction=Faction, FactionValue=FactionValue)

	AdvisorTrigger += """	}
}
"""

file.write(AdvisorsBG)
file1.write(AdvisorsNO)
file2.write(AdvisorsCL)
file3.write(AdvisorsBU)
file4.write(AdvisorsTR)
file5.write(AdvisorsL)
file6.write(AdvisorTrigger)
file7.write(tmp2)
file.close
file2.close
file3.close
file4.close
file5.close
file6.close
file7.close
