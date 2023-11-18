# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import codecs
import math

rights = pd.read_csv('ReformDesire.csv', index_col='Index', sep=';').dropna(how='all').replace({pd.np.nan:None}).to_dict(orient='index')

file = codecs.open('common/scripted_effects/SYS-AI_Reform_Misc.txt', 'w+', encoding='utf-8')

ReformDesireSE = ""
ReformDesireEffect = ""
ReformDoSE = ""
ReformDoEffect = ""
for key in rights.keys():
	
	Right = rights[key]['Right']
	Codename = rights[key]['Codename']
	Ranks = int(rights[key]['Ranks'])
	Interactions = int(rights[key]['Interactions'])
	DefaultPosition = int(rights[key]['DefaultPosition'])

	index = 1

	ReformDesireSE += """AI_ReformDesire{Codename} = {{	#inserteffect
}}
""".format(Codename=Codename)
	ReformDoSE = ""
	ReformDoSE += """AI_ReformDo{Codename} = {{	
	if = {{
        limit = {{
            has_country_flag = AI_Reform_{Codename}

            #check_key = {{ lhs = {Faction}_Mood value = 0 }}
        }}
		#inserteffect
	}}
}}
""".format(Codename=Codename, Faction = Codename[0:2])


	for Rank in range(0,Ranks):
		LvlUp = rights[key]['Lvl'+ str(index)].split(',')[1]
		LvlDown = rights[key]['Lvl'+ str(index)].split(',')[0]
		index += 1

		if(DefaultPosition == 0):
			 CurRank = Rank
		else:
			CurRank = Rank - DefaultPosition + 1
		InversedCodeRank = Ranks - Rank
		if Rank == 0:
			ReformDesireEffect = """	
	if = {{
		limit = {{
			{Codename}{CodeRank}Has = yes
		}}
		set_key = {{ lhs = {Codename}_Ref_Des_Up value = {LvlUp} }}
		change_key = {{ lhs = {Codename}_Ref_Des_Up which = Modi_Add_Rights_{Faction}_Ref_Des_Up }}
		multiply_key = {{ lhs = {Codename}_Ref_Des_Up which = Modi_Multi_Rights_{Faction}_Ref_Des_Up }}
		set_key = {{ lhs = {Codename}_Ref_Des_Down value = {LvlDown} }}
		change_key = {{ lhs = {Codename}_Ref_Des_Up which = Modi_Add_Rights_{Faction}_Ref_Des_Up }}
		multiply_key = {{ lhs = {Codename}_Ref_Des_Down which = Modi_Multi_Rights_{Faction}_Ref_Des_Down }}
	}}""".format(Codename='Rights_'+ Codename,Faction = Codename[0:2],ValueRank=int(CurRank), CodeRank = Rank + 1, LvlUp = LvlUp, LvlDown=LvlDown)
			ReformDoEffect = """	
		if = {{
			limit = {{
			    Rights_{Codename}{InversedCodeRank}RaisePotential = yes 
			}}
			if = {{
			    limit = {{
			        Rights_{Codename}{InversedCodeRank}RaiseAllow = yes
			    }}
			    set_global_flag = AI_ReformLoop

			    Rights_{Codename}{InversedCodeRank}Raise = yes
			}}
		}}""".format(Codename=Codename,ValueRank=int(CurRank), CodeRank = Rank + 1, InversedCodeRank = InversedCodeRank)
		else:
			ReformDesireEffect += """	
	else_if = {{
		limit = {{
			{Codename}{CodeRank}Has = yes
		}}
		set_key = {{ lhs = {Codename}_Ref_Des_Up value = {LvlUp} }}
		change_key = {{ lhs = {Codename}_Ref_Des_Up which = Modi_Add_Rights_{Faction}_Ref_Des_Up }}
		multiply_key = {{ lhs = {Codename}_Ref_Des_Up which = Modi_Multi_Rights_{Faction}_Ref_Des_Up }}
		set_key = {{ lhs = {Codename}_Ref_Des_Down value = {LvlDown} }}
		change_key = {{ lhs = {Codename}_Ref_Des_Up which = Modi_Add_Rights_{Faction}_Ref_Des_Up }}
		multiply_key = {{ lhs = {Codename}_Ref_Des_Down which = Modi_Multi_Rights_{Faction}_Ref_Des_Down }}
	}}""".format(Codename='Rights_'+ Codename,Faction = Codename[0:2],ValueRank=int(CurRank), CodeRank = Rank + 1, LvlUp = LvlUp, LvlDown=LvlDown)
			if Ranks-Rank > 1:
				ReformDoEffect += """	
		else_if = {{
			limit = {{
			    Rights_{Codename}{InversedCodeRank}RaisePotential = yes 
			}}
			if = {{
			    limit = {{
			        Rights_{Codename}{InversedCodeRank}RaiseAllow = yes
			    }}
			    set_global_flag = AI_ReformLoop

			    Rights_{Codename}{InversedCodeRank}Raise = yes

				AI_ReevaluateRightGoals = {{ reform = {Codename} }}
			}}
		}}""".format(Codename=Codename,ValueRank=int(CurRank), CodeRank = Rank + 1, InversedCodeRank = InversedCodeRank, LvlUp = LvlUp, LvlDown=LvlDown)

	ReformDesireSE = ReformDesireSE.replace('#inserteffect', ReformDesireEffect)
	ReformDoSE = ReformDoSE.replace('#inserteffect', ReformDoEffect)
	ReformDesireSE += ReformDoSE


		
file.write(ReformDesireSE)

file.close