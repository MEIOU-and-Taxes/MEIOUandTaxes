# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import codecs

privileges = pd.read_csv('Tools for Modding/Coding/Privswriter/PrivAdd.csv', index_col='Index').dropna(how='all').replace({np.nan:None}).to_dict(orient='index')
privileges2 = pd.read_csv('Tools for Modding/Coding/Privswriter/PrivRevoke.csv', index_col='Index').dropna(how='all').replace({np.nan:None}).to_dict(orient='index')

file = codecs.open('privs_se.txt', 'w+', 	encoding='utf-8')
file2 = codecs.open('privs_seT.txt', 'w+', 	encoding='utf-8')
file3 = codecs.open('privs_seCL.txt', 'w+', encoding='utf-8')
file4 = codecs.open('privs_seL.yml', 'w+', 	encoding='utf-8-sig')
file5 = codecs.open('privs_sePL.txt', 'w+', encoding='utf-8')
Counter = 0
Counter2 = 0
TierL = """l_english:
"""

for key in privileges.keys():
	
	Privilege = privileges[key]['Privilege']
	Codename = privileges[key]['Codename']
	Tiers = int(privileges[key]['Tiers'])
	Nobles = int(privileges[key]['Nobles'])
	Aristocrats = int(privileges[key]['Aristocrats'])
	Burghers = int(privileges[key]['Burghers'])
	Metropolitans = int(privileges[key]['Metropolitans'])
	Clergy = int(privileges[key]['Clergy'])
	Spiritualists = int(privileges[key]['Spiritualists'])
	Clans = int(privileges[key]['Clans'])
	Chiefs = int(privileges[key]['Chiefs'])
	Welfare = int(privileges[key]['Welfare'])
	Bureaucrats = int(privileges[key]['Bureaucrats'])
	LCorruption = int(privileges[key]['LCorruption'])
	SCorruption = int(privileges[key]['SCorruption'])
	Stability = int(privileges[key]['Stability'])
	Nobles2 = int(privileges2[key]['Nobles'])
	Aristocrats2 = int(privileges2[key]['Aristocrats'])
	Burghers2 = int(privileges2[key]['Burghers'])
	Metropolitans2 = int(privileges2[key]['Metropolitans'])
	Clergy2 = int(privileges2[key]['Clergy'])
	Spiritualists2 = int(privileges2[key]['Spiritualists'])
	Clans2 = int(privileges2[key]['Clans'])
	Chiefs2 = int(privileges2[key]['Chiefs'])
	Welfare2 = int(privileges2[key]['Welfare'])
	Bureaucrats2 = int(privileges2[key]['Bureaucrats'])
	LCorruption2 = int(privileges2[key]['LCorruption'])
	SCorruption2 = int(privileges2[key]['SCorruption'])
	Stability2 = int(privileges2[key]['Stability'])
	
	LowerEffect = """
Privilege_{Codename}Lower = {{
	if = {{
   		limit = {{
   			Privilege_Has = {{ Privilege={Codename} Lvl=1 }}
   		}}
		Privilege_{Codename}0LowerReqs = yes
		custom_tooltip = Rights_LB
		custom_tooltip = Privilege_{Codename}0Lower_description
		custom_tooltip = Rights_LB
		if = {{
			limit = {{
				Privilege_{Codename}0CanLower = yes
			}}
			Privilege_{Codename}0Lower = yes
		}}
		else = {{
			tooltip = {{ Privilege_{Codename}0Lower = yes }} # dont actually do it
			[[event]hidden_effect = {{ country_event = {{ id = $event$ }} }}]
		}}
   	}}
""".format(Codename=Codename)

	RaiseEffect = """
Privilege_{Codename}Raise = {{
	if = {{
		limit = {{
			Privilege_Has = {{ Privilege={Codename} Lvl=0 }}
		}}
		Privilege_{Codename}1RaiseReqs = yes
		custom_tooltip = Rights_LB
		custom_tooltip = Privilege_{Codename}1Raise_description
		custom_tooltip = Rights_LB
		if = {{
			limit = {{
				Privilege_{Codename}1CanRaise = yes
			}}
			Privilege_{Codename}1Raise = yes
		}}
		else = {{
			tooltip = {{ Privilege_{Codename}1Raise = yes }} # dont actually do it
			[[event]hidden_effect = {{ country_event = {{ id = $event$ }} }}]
		}}
	}}
""".format(Codename=Codename)
	
	for Tier in range(1,Tiers):
	    LowerEffect += """ 
	else_if = {{
   		limit = {{
   			Privilege_Has = {{ Privilege={Codename} Lvl={NextTier} }}
   		}}
		Privilege_{Codename}{Tier}LowerReqs = yes
		custom_tooltip = Rights_LB
		custom_tooltip = Privilege_{Codename}{Tier}Lower_description
		custom_tooltip = Rights_LB
		if = {{
			limit = {{
				Privilege_{Codename}{Tier}CanLower = yes
			}}
			Privilege_{Codename}{Tier}Lower = yes
		}}
		else = {{
			tooltip = {{ Privilege_{Codename}{Tier}Lower = yes }} # dont actually do it
			[[event]hidden_effect = {{ country_event = {{ id = $event$ }} }}]
		}}
   	}}
""".format(Codename=Codename,Tier=Tier,NextTier=Tier+1)
	
	    RaiseEffect += """
	else_if = {{
		limit = {{
			Privilege_Has = {{ Privilege={Codename} Lvl={Tier} }}
		}}
		Privilege_{Codename}{NextTier}RaiseReqs = yes
		custom_tooltip = Rights_LB
		custom_tooltip = Privilege_{Codename}{NextTier}Raise_description
		custom_tooltip = Rights_LB
		if = {{
			limit = {{
				Privilege_{Codename}{NextTier}CanRaise = yes
			}}
			Privilege_{Codename}{NextTier}Raise = yes
		}}
		else = {{
			tooltip = {{ Privilege_{Codename}{NextTier}Raise = yes }} # dont actually do it
			[[event]hidden_effect = {{ country_event = {{ id = $event$ }} }}]
		}}
	}}
""".format(Codename=Codename,Tier=Tier,NextTier=Tier+1) 
	
	RaiseEffect += """}
	"""
	LowerEffect +="""}
"""
	file.write(LowerEffect)
	file.write(RaiseEffect)
	
	for Tier in range(0,Tiers+1):
		TierEffects = """
Privilege_{Codename}{Tier}Apply = {{
	hidden_effect = {{
		set_key = {{ lhs = Privilege_{Codename} value = {Tier} }}
	}}
}}
""".format(Codename=Codename,Tier=Tier)
		TierEffects2 = """"""
	
		if not Tier == 0:
			TierEffects += """
Privilege_{Codename}{Tier}Raise = {{
	Privilege_{Codename}{Tier}Apply = yes""".format(Codename=Codename,Tier=Tier)
			if Codename[0:2] == "NO":
				TierEffects += """
	Privilege_ManaCost = { mil_power=50 }"""
			elif Codename[0:2] == "BG":
				TierEffects += """
	Privilege_ManaCost = { dip_power=50 }"""
			elif Codename[0:2] == "CL":
				TierEffects += """
	Privilege_ManaCost = { adm_power=50 }"""
			if not Nobles == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=NO Amount={Nobles} }}""".format(Nobles=Nobles)
			if not Aristocrats == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ NO=yes type=value val={Aristocrats} }}""".format(Aristocrats=Aristocrats)
			if not Burghers == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=BG Amount={Burghers} }}""".format(Burghers=Burghers)
			if not Metropolitans == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ BG=yes type=value val={Metropolitans} }}""".format(Metropolitans=Metropolitans)
			if not Clergy == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=CL Amount={Clergy} }}""".format(Clergy=Clergy)
			if not Spiritualists == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ CL=yes type=value val={Spiritualists} }}""".format(Spiritualists=Spiritualists)
			if not Clans == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=TR Amount={Clans} }}""".format(Clans=Clans)
			if not Chiefs == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ TR=yes type=value val={Chiefs} }}""".format(Chiefs=Chiefs)
			if not Welfare == 0:
				TierEffects += """
	Public_ChangeConcernTooltipProv= {{ Concern=Welfare Amount={Welfare} }}""".format(Welfare=Welfare)
			if not Bureaucrats == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ BU=yes type=value val={Bureaucrats} }}""".format(Bureaucrats=Bureaucrats)
			if not LCorruption == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=BU Amount={LCorruption} }}""".format(LCorruption=LCorruption)
			if not SCorruption == 0:
				TierEffects += """
	add_corruption = {SCorruption}""".format(SCorruption=SCorruption)
			if Stability > 0:
				TierEffects += """
	Stab_Add{Stability} = yes""".format(Stability=Stability)
			elif Stability < 0:
				TierEffects += """
	Stab_Subtract{Stability} = yes""".format(Stability=Stability*-1)
			TierEffects += """
}}
Privilege_{Codename}{Tier}RaiseReqs = {{""".format(Codename=Codename,Tier=Tier)
			TierEffects += """
	custom_tooltip = Rights_UI_AllOf
	custom_tooltip = POP_{Powerbroker}""".format(Codename=Codename,Tier=Tier,Powerbroker=Codename[0:2])
			TierEffects += """HasInfluence_30
}
"""
			TierEffects2 += """
Privilege_{Codename}{Tier}CanRaise = {{
	AND = {{""".format(Codename=Codename,Tier=Tier)
			if Codename[0:2] == "NO":
				TierEffects2 += """
		mil_power = 50"""
			elif Codename[0:2] == "BG":
				TierEffects2 += """
		dip_power = 50"""
			elif Codename[0:2] == "CL":
				TierEffects2 += """
		adm_power = 50"""
			TierEffects2 += """
		OR = {{
			Rights_HasSpecialAdvisorOR = {{ Elite={Powerbroker} }}
			faction_influence = {{ faction = FC_{Powerbroker} influence = 30 }}
		}}
	}}
}}
""".format(Codename=Codename,Tier=Tier,Powerbroker=Codename[0:2])
		
		if Tier < Tiers:
			TierEffects += """
Privilege_{Codename}{Tier}Lower = {{
	Privilege_{Codename}{Tier}Apply = yes""".format(Codename=Codename,Tier=Tier)
			if Codename[0:2] == "NO":
				TierEffects += """
	Privilege_ManaCost = { adm_power=25 dip_power=25 mil_power=50 }"""
			elif Codename[0:2] == "BG":
				TierEffects += """
	Privilege_ManaCost = { adm_power=25 dip_power=50 mil_power=25 }"""
			elif Codename[0:2] == "CL":
				TierEffects += """
	Privilege_ManaCost = { adm_power=50 dip_power=25 mil_power=25 }"""
			if not Nobles2 == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=NO Amount={Nobles} }}""".format(Nobles=Nobles2)
			if not Aristocrats2 == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ NO=yes type=value val={Aristocrats} }}""".format(Aristocrats=Aristocrats2)
			if not Burghers2 == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=BG Amount={Burghers} }}""".format(Burghers=Burghers2)
			if not Metropolitans2 == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ BG=yes type=value val={Metropolitans} }}""".format(Metropolitans=Metropolitans2)
			if not Clergy2 == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=CL Amount={Clergy} }}""".format(Clergy=Clergy2)
			if not Spiritualists2 == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ CL=yes type=value val={Spiritualists} }}""".format(Spiritualists=Spiritualists2)
			if not Clans2 == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=TR Amount={Clans} }}""".format(Clans=Clans2)
			if not Chiefs2 == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ TR=yes type=value val={Chiefs} }}""".format(Chiefs=Chiefs2)
			if not Welfare2 == 0:
				TierEffects += """
	Public_ChangeConcernTooltipProv= {{ Concern=Welfare Amount={Welfare} }}""".format(Welfare=Welfare2)
			if not Bureaucrats2 == 0:
				TierEffects += """
	Pol_ChangeRelationsStateTooltip = {{ BU=yes type=value val={Bureaucrats} }}""".format(Bureaucrats=Bureaucrats2)
			if not LCorruption2 == 0:
				TierEffects += """
	Public_ChangePowerbrokerLoyaltyTooltipProv = {{ Powerbroker=BU Amount={LCorruption} }}""".format(LCorruption=LCorruption2)
			if not SCorruption2 == 0:
				TierEffects += """
	add_corruption = {SCorruption}""".format(SCorruption=SCorruption2)
			if Stability2 > 0:
				TierEffects += """
	Stab_Add{Stability} = yes""".format(Stability=Stability2)
			elif Stability2 < 0:
				TierEffects += """
	Stab_Subtract{Stability} = yes""".format(Stability=Stability2*-1)
			TierEffects += """
}}
Privilege_{Codename}{Tier}LowerReqs = {{""".format(Codename=Codename,Tier=Tier)
			TierEffects += """
	custom_tooltip = Rights_UI_NoneOf
	custom_tooltip = POP_{Powerbroker}""".format(Codename=Codename,Tier=Tier,Powerbroker=Codename[0:2])
			if Codename[0:2] == "NO":
				TierEffects += """NotHasInfluence_65
}
"""
			else:
				TierEffects += """NotHasInfluence_50
}
"""
			TierEffects2 += """
Privilege_{Codename}{Tier}CanLower = {{
	AND = {{""".format(Codename=Codename,Tier=Tier)
			if Codename[0:2] == "NO":
				TierEffects2 += """
		adm_power = 25
		dip_power = 25
		mil_power = 50"""
			elif Codename[0:2] == "BG":
				TierEffects2 += """
		adm_power = 25
		dip_power = 50
		mil_power = 25"""
			elif Codename[0:2] == "CL":
				TierEffects2 += """
		adm_power = 50
		dip_power = 25
		mil_power = 25"""
			TierEffects2 += """
		NOT = {{ faction_influence = {{ faction = FC_{Powerbroker} influence = 50 }} }}
    }}
}}
""".format(Codename=Codename,Tier=Tier,Powerbroker=Codename[0:2])
	
		file.write(TierEffects)
		file2.write(TierEffects2)
	TierCL = ""
	for Tier in range(0,Tiers+1):
		TierCL += """
defined_text = {{
	name = Privilege_{Codename}{Tier}Has
	text = {{
		localisation_key = Privilege_{Codename}{Tier}_G
		trigger = {{ Privilege_HasGreater = {{ Privilege={Codename} Lvl={Tier} }} }}
	}}
	text = {{
		localisation_key = Privilege_{Codename}{Tier}_R
		trigger = {{ NOT = {{ Privilege_HasGreater = {{ Privilege={Codename} Lvl={Tier} }} }} }}
	}}
}}
defined_text = {{
	name = Privilege_{Codename}{Tier}NotHas
	text = {{
		localisation_key = Privilege_{Codename}{Tier}_G
		trigger = {{ NOT = {{ Privilege_HasGreater = {{ Privilege={Codename} Lvl={Tier} }} }} }}
	}}
	text = {{
		localisation_key = Privilege_{Codename}{Tier}_R
		trigger = {{ Privilege_HasGreater = {{ Privilege={Codename} Lvl={Tier} }} }}
	}}
}}
""".format(Codename=Codename,Tier=Tier)
	for Tier in range(0,Tiers+1):
		TierCL += """
defined_text = {{
	name = Privilege_{Codename}{Tier}_title
	text = {{
		localisation_key = Privilege_{Codename}{Tier}_g
		trigger = {{ Privilege_Has = {{ Privilege={Codename} Lvl={Tier} }} }}
	}}
	text = {{
		localisation_key = Privilege_{Codename}{Tier}_o
		trigger = {{ NOT = {{ Privilege_Has = {{ Privilege={Codename} Lvl={Tier} }} }} }}
	}}
}}
""".format(Codename=Codename,Tier=Tier)
	for Tier in range(0,Tiers):
		TierCL += """
defined_text = {{
	name = Privilege_{Codename}{Tier}LowerAllow
	text = {{
		localisation_key = Privilege_{Codename}{Tier}LowerAllow_Y
		trigger = {{ Privilege_{Codename}{Tier}CanLower = yes }}
	}}
	text = {{
		localisation_key = Privilege_{Codename}{Tier}LowerAllow_N
		trigger = {{ Privilege_{Codename}{Tier}CanLower = no }}
	}}
}}
""".format(Codename=Codename,Tier=Tier)
	for Tier in range(1,Tiers+1):
		TierCL += """
defined_text = {{
	name = Privilege_{Codename}{Tier}RaiseAllow
	text = {{
		localisation_key = Privilege_{Codename}{Tier}RaiseAllow_Y
		trigger = {{ Privilege_{Codename}{Tier}CanRaise = yes }}
	}}
	text = {{
		localisation_key = Privilege_{Codename}{Tier}RaiseAllow_N
		trigger = {{ Privilege_{Codename}{Tier}CanRaise = no }}
	}}
}}
""".format(Codename=Codename,Tier=Tier)
	TierCL += """
defined_text = {{
	name = Privilege_{Codename}Lower_title
""".format(Codename=Codename,Tier=Tier)
	for Tier in range(0,Tiers):
		TierCL += """	text = {{
		localisation_key = Privilege_{Codename}{Tier}Lower_title
		trigger = {{
			Privilege_Has = {{ Privilege={Codename} Lvl={NextTier} }}
			Privilege_{Codename}{Tier}CanLower = yes
		}}
	}}
	text = {{
		localisation_key = Privilege_{Codename}{Tier}Lower_title_g
		trigger = {{
			Privilege_Has = {{ Privilege={Codename} Lvl={NextTier} }}
			Privilege_{Codename}{Tier}CanLower = no
		}}
	}}
""".format(Codename=Codename,Tier=Tier,NextTier=Tier+1)
	TierCL += """}"""
	TierCL += """
defined_text = {{
	name = Privilege_{Codename}Raise_title
""".format(Codename=Codename,Tier=Tier)
	for Tier in range(1,Tiers+1):
		TierCL += """	text = {{
		localisation_key = Privilege_{Codename}{Tier}Raise_title
		trigger = {{
			Privilege_Has = {{ Privilege={Codename} Lvl={PrevTier} }}
			Privilege_{Codename}{Tier}CanRaise = yes
		}}
	}}
	text = {{
		localisation_key = Privilege_{Codename}{Tier}Raise_title_g
		trigger = {{
			Privilege_Has = {{ Privilege={Codename} Lvl={PrevTier} }}
			Privilege_{Codename}{Tier}CanRaise = no
		}}
	}}
""".format(Codename=Codename,Tier=Tier,PrevTier=Tier-1)
	TierCL += """}"""
	TierCL += """
defined_text = {{
	name = Privilege_{Codename}_d
	text = {{
		localisation_key = Privilege_{Codename}_d
		trigger = {{ always = yes }}
	}}
}}""".format(Codename=Codename)
	TierCL += """
defined_text = {{
	name = Privilege_{Codename}Num
""".format(Codename=Codename,Tier=Tier)
	for Tier in range(0,Tiers+1):
		TierCL += """	text = {{
		localisation_key = Rights_{Tier}
		trigger = {{ Privilege_Has = {{ Privilege={Codename} Lvl={Tier} }} }}
	}}
""".format(Codename=Codename,Tier=Tier,PrevTier=Tier-1)
	TierCL += """}"""
	file3.write(TierCL)
	TierL += """ Privilege_{Codename}: "§G{Privilege}§!"
 Privilege_{Codename}_t: "{Privilege}"
 Privilege_{Codename}_d: "*{Codename}Desc*"
 Privilege_{Codename}_n: "{Privilege} §Y([Privilege_{Codename}Num])§!"
 Privilege_{Codename}Raise_title: "[Privilege_{Codename}Raise_title]"
 Privilege_{Codename}Lower_title: "[Privilege_{Codename}Lower_title]"
""".format(Codename=Codename,Privilege=Privilege)
	for Tier in range(0,Tiers+1):
		TierL += """ Privilege_{Codename}{Tier}_t: "§Y*{Codename}{Tier}Title* ({Tier})§!"
 Privilege_{Codename}{Tier}_title: "[Privilege_{Codename}{Tier}_title]"
 Privilege_{Codename}{Tier}_o: "§g*{Codename}{Tier}Title* ({Tier})§!"
 Privilege_{Codename}{Tier}_g: "§G*{Codename}{Tier}Title* ({Tier})§!"
 Privilege_{Codename}{Tier}_description: "*{Codename}{Tier}Desc*"
""".format(Codename=Codename,Tier=Tier)
		if Tier > 0:
			TierL += """ Privilege_{Codename}{Tier}_effects: "\\n§YEffects§!\\n*{Codename}{Tier}Effects*"
""".format(Codename=Codename,Tier=Tier)
		else:
			TierL += """ Privilege_{Codename}{Tier}_effects: "§YNo effects§!"
""".format(Codename=Codename,Tier=Tier)
		if Tier < Tiers:
			TierL += """ Privilege_{Codename}{Tier}Lower_title: "*{Codename}{Tier}TitleLower*"
 Privilege_{Codename}{Tier}Lower_title_g: "§g*{Codename}{Tier}TitleLower*§!"
 Privilege_{Codename}{Tier}Lower_effects: "\\n§YEffects§!\\n*{Codename}{Tier}EffectsLower*"
 Privilege_{Codename}{Tier}Lower_description: "Transition from §Y*{Codename}{NextTier}Title* ({NextTier})§! to §Y*{Codename}{Tier}Title* ({Tier}) §!\\n§G{Privilege}§!\\n*{Codename}{Tier}Desc*\\n\\n§YEffects§!\\n*{Codename}{Tier}EffectsLower*"
""".format(Codename=Codename,Tier=Tier,NextTier=Tier+1,Privilege=Privilege)
		if Tier > 0:
			TierL += """ Privilege_{Codename}{Tier}Raise_title: "*{Codename}{Tier}TitleRaise*"
 Privilege_{Codename}{Tier}Raise_title_g: "§g*{Codename}{Tier}TitleRaise*§!"
 Privilege_{Codename}{Tier}Raise_effects: "\\n§YEffects§!\\n*{Codename}{Tier}EffectsRaise*"
 Privilege_{Codename}{Tier}Raise_description: "Transition from §Y*{Codename}{PrevTier}Title* ({PrevTier})§! to §Y*{Codename}{Tier}Title* ({Tier}) §!\\n§G{Privilege}§!\\n*{Codename}{Tier}Desc*\\n\\n§YEffects§!\\n*{Codename}{Tier}EffectsRaise*"
""".format(Codename=Codename,Tier=Tier,PrevTier=Tier-1,Privilege=Privilege)
		if Codename[0:2] == "NO":
			TierL += """ Privilege_{Codename}{Tier}Has: "[Privilege_{Codename}{Tier}Has]"
 Privilege_{Codename}{Tier}NotHas: "[Privilege_{Codename}{Tier}NotHas]" 
 Privilege_{Codename}{Tier}HasGreater: "£estate_greater_nobles_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}HasGreaterNOT: "NOT £estate_greater_nobles_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}_G: "§G - {Privilege}: £estate_greater_nobles_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
 Privilege_{Codename}{Tier}_R: "§R - {Privilege}: £estate_greater_nobles_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
""".format(Codename=Codename,Tier=Tier,Privilege=Privilege)
		elif Codename[0:2] == "BG":
			TierL += """ Privilege_{Codename}{Tier}Has: "[Privilege_{Codename}{Tier}Has]"
 Privilege_{Codename}{Tier}NotHas: "[Privilege_{Codename}{Tier}NotHas]" 
 Privilege_{Codename}{Tier}HasGreater: "£estate_city_burghers_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}HasGreaterNOT: "NOT £estate_city_burghers_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}_G: "§G - {Privilege}: £estate_city_burghers_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
 Privilege_{Codename}{Tier}_R: "§R - {Privilege}: £estate_city_burghers_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
""".format(Codename=Codename,Tier=Tier,Privilege=Privilege)
		elif Codename[0:2] == "CL":
			TierL += """ Privilege_{Codename}{Tier}Has: "[Privilege_{Codename}{Tier}Has]"
 Privilege_{Codename}{Tier}NotHas: "[Privilege_{Codename}{Tier}NotHas]" 
 Privilege_{Codename}{Tier}HasGreater: "£estate_church_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}HasGreaterNOT: "NOT £estate_church_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}_G: "§G - {Privilege}: £estate_church_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
 Privilege_{Codename}{Tier}_R: "§R - {Privilege}: £estate_church_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
""".format(Codename=Codename,Tier=Tier,Privilege=Privilege)
		elif Codename[0:2] == "BU":
			TierL += """ Privilege_{Codename}{Tier}Has: "[Privilege_{Codename}{Tier}Has]"
 Privilege_{Codename}{Tier}NotHas: "[Privilege_{Codename}{Tier}NotHas]" 
 Privilege_{Codename}{Tier}HasGreater: "£estate_bureaucracy_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}HasGreaterNOT: "NOT £estate_bureaucracy_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}_G: "§G - {Privilege}: £estate_bureaucracy_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
 Privilege_{Codename}{Tier}_R: "§R - {Privilege}: £estate_bureaucracy_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
""".format(Codename=Codename,Tier=Tier,Privilege=Privilege)
	file4.write(TierL)
	TierL = ""
	TierPL = ""
	for Tier in range(0,Tiers+1):
		TierPL += """Privilege_{Codename}{Tier}
""".format(Codename=Codename,Tier=Tier)
	file5.write(TierPL)

file.close
file2.close
file3.close
file4.close
file5.close
