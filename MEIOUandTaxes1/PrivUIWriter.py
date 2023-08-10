# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import codecs
import math

privilege = pd.read_csv('PrivilegeRaise.csv', index_col='Index', sep=';').dropna(how='all').replace({pd.np.nan:None}).to_dict(orient='index')
privilege_lower = pd.read_csv('PrivilegeLower.csv', index_col='Index', sep=';').dropna(how='all').replace({pd.np.nan:None}).to_dict(orient='index')

file = codecs.open('common/estate_privileges/00_privileges.txt', 'w+', encoding='utf-8')
file2 = codecs.open('common/scripted_effects/SYS-PrivilegesUIAssign.txt', 'w+', encoding='utf-8')
file3 = codecs.open('PrivilegeUIList.txt', 'w+', encoding='utf-8')
file4 = codecs.open('localisation/SYS-Privilege_UI_l_english.yml', 'w+', encoding='utf-8-sig')
file5 = codecs.open('events/SYS-Privilege.txt', 'w+', 	encoding='utf-8')
file6 = codecs.open('gfx.txt', 'w+', 	encoding='utf-8')

loc_input = codecs.open('localisation/SYS-Privileges_l_english.yml', 'r', encoding='utf-8-sig')

base_loc = loc_input.readlines()

tmp_gfx = ""

PrivilegeP = ""
PrivilegeList =""
PrivilegeAssign = """
PrivilegeUI_Assign = {
"""
PrivilegeL = """l_english:
"""
PrivilegeEvents = """namespace = Privilege
country_event = {
	id = Privilege.998
	title = no_localization
	desc = no_localization
	picture = ai_only
	is_triggered_only = yes
	hidden = yes

	immediate = {
		set_country_flag = Reset_UI
		if = {
			limit = {
				ai = no
			}
			PrivilegeUI_Assign = yes
			Nat_Display = yes
		}
	}
	option = {
		name = PTM_EXIT
	}
}
country_event = { # triggered by monthly pulse
	id = Privilege.999
	title = no_localization
	desc = no_localization
	picture = ai_only
	is_triggered_only = yes
	hidden = yes

	immediate = {
		every_country = {
			limit = {
				ai = no
				isValidCountry = yes
			}
			set_country_flag = Reset_UI
			PrivilegeUI_Assign = yes
			Nat_Display = yes
		}		
	}
	option = {
		name = PTM_EXIT
	}
}

"""
PrivilegeCustomLoc = ""
Counter = 0
for key in privilege.keys():
	
	Right = privilege[key]['Privilege']
	Codename = privilege[key]['Codename']
	Ranks = int(privilege[key]['Ranks'])
	Interactions = int(privilege[key]['Interactions'])
	DefaultPosition = int(privilege[key]['DefaultPosition'])
	Icon = privilege[key]['Icon']
	Event = privilege[key]['Event']

	Counter += 1
	Events_Tmp = ""
	Events_Tmp += """
country_event = {{
	id = Privilege.{Counter}
	title = Privilege_{Codename}_t
	desc = Privilege_{Codename}_d""".format(Codename=Codename,Counter=Counter)
	if Codename[0:2] == "NO":
		Events_Tmp += """
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
		Events_Tmp += """
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
		Events_Tmp += """
	picture = all_church_state
"""
	elif Codename[0:2] == "TR":
		Events_Tmp += """
	picture = { trigger = { OR = { technology_group = chinese technology_group = japanese technology_group = southeast_asian technology_group = tibetan technology_group = ottoman technology_group = western technology_group = eastern technology_group = byzantine technology_group = indian technology_group = steppestech } } picture = MON_TRI_eventPicture }
	picture = { trigger = { OR = { technology_group = muslim technology_group = soudantech } } picture = ARAB_TRI_eventPicture }
	picture = { trigger = { OR = { technology_group = sub_saharan technology_group = central_african technology_group = malagasy_tech technology_group = east_african } } picture = AFR_LN_eventPicture }
	picture = { trigger = { OR = { technology_group = austranesian technology_group = hawaii_tech  } } picture = SEA_LN_eventPicture }
	picture = { trigger = { OR = { technology_group = mesoamerican technology_group = south_american } } picture = AMR_LN_eventPicture }
"""
	elif Codename[0:2] == "BU":
		Events_Tmp += """
	picture = ECONOMY_eventPicture		
"""
	Events_Tmp += """
	is_triggered_only = yes
	
	immediate = {
        hidden_effect = { set_country_flag = Privilege_Change }
	}
"""
	Events_Tmp += """
	# Raise
	option = {{
		name = Privilege_{Codename}Raise_title
		trigger = {{
   			NOT = {{ Privilege_Has = {{ Privilege={Codename} Lvl={LastRank} }} }}
		}}
		Privilege_{Codename}Raise = yes
		custom_tooltip = Privilege_UI_Info
		hidden_effect = {{
			Nat_Update = yes
		}}
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
		custom_tooltip = Privilege_UI_Info
		hidden_effect = {{
			Nat_Update = yes
		}}
		ai_chance = {{
			factor = 0
		}}
	}}
	option = {{
		name = PTM_EXIT
		
	}}
    after = {{ 
        clr_country_flag = Privilege_Change
		remove_country_modifier = Prov_PrivilegeUIBlock
    }}
}}""".format(Codename=Codename,LastRank=Ranks-1)
	PrivilegeEvents += Events_Tmp

	for Rank in range(0,Ranks):
		if(DefaultPosition == 0):
			 CurRank = Rank
		else:
			CurRank = Rank - DefaultPosition + 1
		PrivilegeP += """
Privilege_{Codename}{CodeRank} = {{
	icon = {Codename}_{CodeRank}
	land_share = 0
	max_absolutism = 0
	loyalty = 0
	influence = 0
	can_select = {{
		hidden_trigger = {{ ai = no }}
        Privilege_Has = {{ Privilege={Codename} Lvl={ValueRank} }}
	}}
	can_revoke = {{
		custom_trigger_tooltip = {{
			tooltip = Pow_{Elite}Change
			NOT = {{ has_country_modifier = Prov_{Elite}Block }}
		}}
		custom_trigger_tooltip = {{
			tooltip = Pow_PrivilegeChange
			NOT = {{ has_country_modifier = Prov_PrivilegeUIBlock }}
		}}
	}}
	on_granted = {{
	}}
	on_revoked = {{
		custom_tooltip = Privilege_{Codename}{CodeRank}_description # Rank Description
		custom_tooltip = Privilege_{Codename}{CodeRank}_effects # Main Effects
		hidden_effect = {{
			if = {{
				limit = {{
					NOT = {{ has_country_flag = Privilege_Change }}
					NOT = {{ has_country_flag = Reset_UI }}
				}}
				country_event = {{ id = Privilege.{Counter} }}
				add_country_modifier = {{ name = Prov_PrivilegeUIBlock duration = -1 hidden=yes }}
			}}
		}}
    }}
	penalties = {{
	}}
	benefits = {{
	}}
	ai_will_do = {{
		factor = 0
	}}
}}
""".format(Codename=Codename,ValueRank=int(CurRank), CodeRank = Rank, Counter = Counter, Elite=Codename[0:2])
		PrivilegeList += """{Codename}{Rank}
""".format(Codename='Privilege_' + Codename,Rank=Rank)

		tmp_gfx += """spriteType = {{
	name = "Privilege_{Codename}_{Rank}"
	texturefile = "gfx/interface/estates/privileges/{Codename}_{Rank}.png"
}}
""".format(Codename=Codename,Rank=Rank)

	## Create Localisation for Privilege Titles
	for Rank in range(0,Ranks):
		i = 0
		SearchGenTitle = ' Privilege_' + Codename
		SearchNumTitle = ' Privilege_' + Codename + str(Rank) + '_t'
		for loc in base_loc:
			try:
				if loc.split(':')[0] == SearchGenTitle:
					index_gen_title = i
			except Exception:
				pass  # or you could use 'continue'
			
			try:
				if loc.split(':')[0] == SearchNumTitle:
					index_num_title = i
			except Exception:
				pass  # or you could use 'continue'
			i += 1
		
		if index_gen_title != -1:
			GenTitle = base_loc[index_gen_title].replace('\n', '').replace('\r', '')
			GenTitle = GenTitle.split(':')[1]
			GenTitle = GenTitle.split('"')[1] + GenTitle.split('"')[2]
		if index_num_title != -1:
			NumTitle = base_loc[index_num_title].replace('\n', '').replace('\r', '')
			NumTitle = NumTitle.split(':')[1]
			NumTitle = NumTitle.split('"')[1] + NumTitle.split('"')[2]

		PrivilegeL += """ {Codename}{Rank}:1 "{num_title}\\n{gen_title}"
 {Codename}{Rank}_mod:1 "{gen_title}: {num_title}"
 {Codename}{Rank}_desc:1 "[{Codename}_d]"
""".format(Codename='Privilege_' + Codename,Rank=Rank, gen_title = GenTitle, num_title = NumTitle)		
	## Create Reset effects
	for Rank in range(0,Ranks):
		if(DefaultPosition == 0):
			 CurRank = Rank
		else:
			CurRank = Rank - DefaultPosition + 1 
		PrivilegeAssign += """	remove_estate_privilege = Privilege_{Codename}{CodeRank}
"""	.format(Codename=Codename,ValueRank=int(CurRank), CodeRank = Rank)

	## Create Assignment effects
	for Rank in range(0,Ranks):
		if(DefaultPosition == 0):
			 CurRank = Rank
		else:
			CurRank = Rank - DefaultPosition + 1 
		if(Rank == 0):
			PrivilegeAssign += """    if = {{
        limit = {{
            Privilege_Has = {{ Privilege={Codename} Lvl={ValueRank} }}
        }}
        set_estate_privilege = Privilege_{Codename}{CodeRank}
    }}
"""	.format(Codename=Codename,ValueRank=int(CurRank), CodeRank = Rank)
		else:
			PrivilegeAssign += """    else_if = {{
        limit = {{
            Privilege_Has = {{ Privilege={Codename} Lvl={ValueRank} }}
        }}
		set_estate_privilege = Privilege_{Codename}{CodeRank}
    }}
""".format(Codename=Codename,ValueRank=int(CurRank), CodeRank = Rank)

PrivilegeAssign += """	clr_country_flag = Reset_UI
}"""
	
file.write(PrivilegeP)
file2.write(PrivilegeAssign)
file3.write(PrivilegeList)
file4.write(PrivilegeL)
file5.write(PrivilegeEvents)
file6.write(tmp_gfx)


file.close
file2.close
file3.close
file4.close
file5.close