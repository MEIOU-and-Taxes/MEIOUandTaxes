# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import codecs

privileges = pd.read_csv('PrivAdd.csv', index_col='Index').dropna(how='all').replace({pd.np.nan:None}).to_dict(orient='index')
privileges2 = pd.read_csv('PrivRevoke.csv', index_col='Index').dropna(how='all').replace({pd.np.nan:None}).to_dict(orient='index')

file = codecs.open('privs_se.txt', 'w+', 	encoding='utf-8')
file2 = codecs.open('privs_seT.txt', 'w+', 	encoding='utf-8')
file3 = codecs.open('privs_seCL.txt', 'w+', encoding='utf-8')
file4 = codecs.open('privs_seL.yml', 'w+', 	encoding='utf-8-sig')
file5 = codecs.open('privs_seP.txt', 'w+', 	encoding='utf-8')
file6 = codecs.open('privs_seE.txt', 'w+', 	encoding='utf-8')
file7 = codecs.open('privs_sePL.txt', 'w+', encoding='utf-8')
file8 = codecs.open('common/scripted_effects/SYS-PrivilegesAssign.txt', 'w+', 	encoding='utf-8')
Counter = 0
Counter2 = 0
TierL = """l_english:
"""
TierS = """
Privilege_Assign = {
"""
file8.write(TierS)

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
		custom_tooltip = Privilege_{Codename}0Lower_desc
		custom_tooltip = Rights_LB
		if = {{
			limit = {{
				Privilege_{Codename}0CanLower = yes
			}}
			Privilege_{Codename}0Lower = yes
            hidden_effect = {{ remove_estate_privilege = Privilege_{Codename}1 }}
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
		custom_tooltip = Privilege_{Codename}1Raise_desc
		custom_tooltip = Rights_LB
		if = {{
			limit = {{
				Privilege_{Codename}1CanRaise = yes
			}}
			Privilege_{Codename}1Raise = yes
            hidden_effect = {{ remove_estate_privilege = Privilege_{Codename}0 }}
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
		custom_tooltip = Privilege_{Codename}{Tier}Lower_desc
		custom_tooltip = Rights_LB
		if = {{
			limit = {{
				Privilege_{Codename}{Tier}CanLower = yes
			}}
			Privilege_{Codename}{Tier}Lower = yes
            hidden_effect = {{ remove_estate_privilege = Privilege_{Codename}{NextTier} }}
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
		custom_tooltip = Privilege_{Codename}{NextTier}Raise_desc
		custom_tooltip = Rights_LB
		if = {{
			limit = {{
				Privilege_{Codename}{NextTier}CanRaise = yes
			}}
			Privilege_{Codename}{NextTier}Raise = yes
            hidden_effect = {{ remove_estate_privilege = Privilege_{Codename}{Tier} }}
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
        set_estate_privilege = Privilege_{Codename}{Tier}
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
			if not Stability == 0:
				TierEffects += """
	Stab_Add{Stability} = yes""".format(Stability=Stability)
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
			if not Stability2 == 0:
				TierEffects += """
	Stab_Add{Stability} = yes""".format(Stability=Stability2)
			TierEffects += """
}}
Privilege_{Codename}{Tier}LowerReqs = {{""".format(Codename=Codename,Tier=Tier)
			TierEffects += """
	custom_tooltip = Rights_UI_NoneOf
	custom_tooltip = POP_{Powerbroker}""".format(Codename=Codename,Tier=Tier,Powerbroker=Codename[0:2])
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
 Privilege_{Codename}{Tier}_desc: "*{Codename}{Tier}Desc*"
""".format(Codename=Codename,Tier=Tier)
		if Tier > 0:
			TierL += """ Privilege_{Codename}{Tier}_effects: "\\n§YEffects§!\\n*{Codename}{Tier}Effects*"
""".format(Codename=Codename,Tier=Tier)
		if Tier < Tiers:
			TierL += """ Privilege_{Codename}{Tier}Lower_title: "*{Codename}{Tier}TitleLower*"
 Privilege_{Codename}{Tier}Lower_title_g: "§g*{Codename}{Tier}TitleLower*§!"
 Privilege_{Codename}{Tier}Lower_effects: "\\n§YEffects§!\\n*{Codename}{Tier}EffectsLower*"
 Privilege_{Codename}{Tier}Lower_desc: "Transition from §Y*{Codename}{NextTier}Title* ({NextTier})§! to §Y*{Codename}{Tier}Title* ({Tier}) §!\\n§G{Privilege}§!\\n*{Codename}{Tier}Desc*\\n\\n§YEffects§!\\n*{Codename}{Tier}EffectsLower*"
""".format(Codename=Codename,Tier=Tier,NextTier=Tier+1,Privilege=Privilege)
		if Tier > 0:
			TierL += """ Privilege_{Codename}{Tier}Raise_title: "*{Codename}{Tier}TitleRaise*"
 Privilege_{Codename}{Tier}Raise_title_g: "§g*{Codename}{Tier}TitleRaise*§!"
 Privilege_{Codename}{Tier}Raise_effects: "\\n§YEffects§!\\n*{Codename}{Tier}EffectsRaise*"
 Privilege_{Codename}{Tier}Raise_desc: "Transition from §Y*{Codename}{PrevTier}Title* ({PrevTier})§! to §Y*{Codename}{Tier}Title* ({Tier}) §!\\n§G{Privilege}§!\\n*{Codename}{Tier}Desc*\\n\\n§YEffects§!\\n*{Codename}{Tier}EffectsRaise*"
""".format(Codename=Codename,Tier=Tier,PrevTier=Tier-1,Privilege=Privilege)
		TierL += """ Privilege_{Codename}{Tier}Has: "[Privilege_{Codename}{Tier}Has]"
 Privilege_{Codename}{Tier}NotHas: "[Privilege_{Codename}{Tier}NotHas]" 
 Privilege_{Codename}{Tier}HasGreater: "£estate_greater_nobles_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}HasGreaterNOT: "NOT £estate_greater_nobles_icon_small£ §G{Privilege}:§! *{Codename}{Tier}Title* §Y({Tier})+§!"
 Privilege_{Codename}{Tier}_G: "§G - Privilege: £estate_greater_nobles_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
 Privilege_{Codename}{Tier}_R: "§R - Privilege: £estate_greater_nobles_icon_small£ *{Codename}{Tier}Title*§! §Y({Tier})§!"
""".format(Codename=Codename,Tier=Tier,Privilege=Privilege)
	file4.write(TierL)
	TierL = ""
	TierP = ""
	Counter += 1
	for Tier in range(0,Tiers+1):
		TierP += """
Privilege_{Codename}{Tier} = {{
	icon = privilege_grant_autonomy
	land_share = 0
	max_absolutism = 0
	loyalty = 0
	influence = 0
	can_select = {{
        Privilege_Has = {{ Privilege={Codename} Lvl={Tier} }}
	}}
	on_granted = {{
	}}
	on_revoked = {{
        hidden_effect = {{ if = {{ limit = {{ NOT = {{ has_country_flag = Privilege_Change }} }} country_event = {{ id = Privilege.{Counter} }} }} }}
    }}
	penalties = {{
	}}
	benefits = {{
	}}
	ai_will_do = {{
		factor = 0
	}}
}}""".format(Codename=Codename,Tier=Tier,Counter=Counter)
	file5.write(TierP)
	TierE = ""
	TierE += """
country_event = {{
	id = Privilege.{Counter}
	title = Privilege_{Codename}_t
	desc = Privilege_{Codename}_d""".format(Codename=Codename,Counter=Counter)
	if Codename[0:2] == "NO":
		TierE += """
	picture = { trigger = { technology_group = western } picture = WE_GN_eventPicture }
	picture = { trigger = { OR = { technology_group = muslim technology_group = ottoman technology_group = steppestech } } picture = ISL_GN_eventPicture }
	picture = { trigger = { OR = { technology_group = eastern technology_group = byzantine } } picture = EE_GN_eventPicture }
	picture = { trigger = { technology_group = indian } picture = IND_GN_eventPicture }
	picture = { trigger = { OR = { technology_group = chinese technology_group = japanese technology_group = southeast_asian technology_group = tibetan } } picture = EA_GN_eventPicture }
	picture = { trigger = { OR = { technology_group = soudantech technology_group = sub_saharan technology_group = central_african technology_group = malagasy_tech technology_group = east_african } } picture = AFR_GN_eventPicture }
	picture = { trigger = { OR = { technology_group = austranesian technology_group = hawaii_tech } } picture = SEA_GN_eventPicture }
	picture = { trigger = { OR = { technology_group = mesoamerican technology_group = south_american } } picture = AMR_GN_eventPicture }
"""
	elif Codename[0:2] == "BG":
		TierE += """
	picture = { trigger = { technology_group = western } picture = WE_BUR_eventPicture }
	picture = { trigger = { OR = { technology_group = muslim technology_group = ottoman technology_group = steppestech } } picture = ISL_BUR_eventPicture }
	picture = { trigger = { OR = { technology_group = eastern technology_group = byzantine } } picture = EE_BUR_eventPicture }
	picture = { trigger = { technology_group = indian } picture = IND_BUR_eventPicture }
	picture = { trigger = { OR = { technology_group = chinese technology_group = japanese technology_group = southeast_asian technology_group = tibetan } } picture = EA_BUR_eventPicture }
	picture = { trigger = { OR = { technology_group = soudantech technology_group = sub_saharan technology_group = central_african technology_group = malagasy_tech technology_group = east_african } } picture = AFR_BUR_eventPicture }
	picture = { trigger = { OR = { technology_group = austranesian technology_group = hawaii_tech } } picture = SEA_BUR_eventPicture }
	picture = { trigger = { OR = { technology_group = mesoamerican technology_group = south_american } } picture = AMR_BUR_eventPicture }
"""
	elif Codename[0:2] == "CL":
		TierE += """
	picture = all_church_state
"""
	elif Codename[0:2] == "TR":
		TierE += """
	picture = { trigger = { OR = { technology_group = chinese technology_group = japanese technology_group = southeast_asian technology_group = tibetan technology_group = ottoman technology_group = western technology_group = eastern technology_group = byzantine technology_group = indian technology_group = steppestech } } picture = MON_TRI_eventPicture }
	picture = { trigger = { OR = { technology_group = muslim technology_group = soudantech } } picture = ARAB_TRI_eventPicture }
	picture = { trigger = { OR = { technology_group = sub_saharan technology_group = central_african technology_group = malagasy_tech technology_group = east_african } } picture = AFR_LN_eventPicture }
	picture = { trigger = { OR = { technology_group = austranesian technology_group = hawaii_tech  } } picture = SEA_LN_eventPicture }
	picture = { trigger = { OR = { technology_group = mesoamerican technology_group = south_american } } picture = AMR_LN_eventPicture }
"""
	TierE += """
	is_triggered_only = yes
	
	immediate = {
        hidden_effect = { set_country_flag = Privilege_Change }
	}
"""
	TierE += """
	# Raise
	option = {{
		name = Privilege_{Codename}Raise_title
		trigger = {{
   			NOT = {{ Privilege_Has = {{ Privilege={Codename} Lvl={LastTier} }} }}
		}}
		Privilege_{Codename}Raise = yes
		ai_chance = {{
			factor = 0
		}}
	}}
	# Lower
	option = {{
		name = Privilege_{Codename}Lower_title
		trigger = {{
   			NOT = {{ Privilege_Has = {{ Privilege={Codename} Lvl=0 }} }}
		}}
		Privilege_{Codename}Lower = yes
		ai_chance = {{
			factor = 0
		}}
	}}
    after = {{ 
        clr_country_flag = Privilege_Change
    }}
}}""".format(Codename=Codename,LastTier=Tiers)
	file6.write(TierE)
	TierPL = ""
	for Tier in range(0,Tiers+1):
		TierPL += """Privilege_{Codename}{Tier}
""".format(Codename=Codename,Tier=Tier)
	file7.write(TierPL)
	TierS = ""
	TierS += """    if = {{
        limit = {{
            Privilege_Has = {{ Privilege={Codename} Lvl=0 }}
        }}
        set_estate_privilege = Privilege_{Codename}0
    }}
""".format(Codename=Codename)
	for Tier in range(1,Tiers+1):
		TierS += """    else_if = {{
        limit = {{
            Privilege_Has = {{ Privilege={Codename} Lvl={Tier} }}
        }}
        set_estate_privilege = Privilege_{Codename}{Tier}
    }}
""".format(Codename=Codename,Tier=Tier)
	file8.write(TierS)

TierS = """}"""
file8.write(TierS)

file.close
file2.close
file3.close
file4.close
file5.close
file6.close
file7.close
file8.close
