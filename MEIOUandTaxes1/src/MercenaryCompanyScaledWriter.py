# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import codecs
import math

scaling = pd.read_csv('MercenaryScaling.csv', index_col='Index', sep=';').dropna(how='all').replace({pd.np.nan:None}).to_dict(orient='index')

file = codecs.open('common/mercenary_companies/01_ScaledMercenaryCompanies.txt', 'w+', encoding='utf-8')
file2 = codecs.open('localisation/MEC-military_mercenary_companies_l_english.yml', 'w+', encoding='utf-8-sig')

Company = ""
CompanyL = """l_english:
"""

for key in scaling.keys():

	MinDev = int(scaling[key]['MinDev'])
	MaxDev = int(scaling[key]['MaxDev'])
	SmallScaling = float(scaling[key]['SmallScaling'])
	MedScaling = float(scaling[key]['MedScaling'])
	LargeScaling = float(scaling[key]['LargeScaling'])

	Company += """merc_dev_{MinDev}_{MaxDev}_small = {{
	regiments_per_development = {Scaling}
	cavalry_weight = 0.1
	artillery_weight = 0.1
	cavalry_cap = 2
	cost_modifier = 1.0
	trigger = {{
		capital_scope = {{
			OR = {{
				continent = europe
				continent = mena
				continent = africa
			}}
		}}
		Rights_BUSer3HasGreater = no
		OR = {{
			NOT = {{ stability = 0 }}
			NOT = {{ corruption = 40 }}
			has_any_disaster = no
			NOT = {{ num_of_loans = 3 }}
		}}
		total_development = {MinDev}
		NOT = {{ total_development = {MaxDev} }}
	}}
	# No home province means local mercenary company
}}
""".format(MinDev = MinDev, MaxDev= MaxDev, Scaling=SmallScaling)

	Company += """merc_dev_{MinDev}_{MaxDev}_med = {{
	regiments_per_development = {Scaling}
	cavalry_weight = 0.1
	artillery_weight = 0.1
	cavalry_cap = 2
	cost_modifier = 1.0
	trigger = {{
		capital_scope = {{
			OR = {{
				continent = europe
				continent = mena
				continent = africa
			}}
		}}
		Rights_BUSer3HasGreater = no
		OR = {{
			NOT = {{ stability = 0 }}
			NOT = {{ corruption = 40 }}
			has_any_disaster = no
			NOT = {{ num_of_loans = 3 }}
		}}
		total_development = {MinDev}
		NOT = {{ total_development = {MaxDev} }}
	}}
	# No home province means local mercenary company
}}
""".format(MinDev = MinDev, MaxDev= MaxDev, Scaling=MedScaling)
	Company += """merc_dev_{MinDev}_{MaxDev}_large = {{
	regiments_per_development = {Scaling}
	cavalry_weight = 0.1
	artillery_weight = 0.1
	cavalry_cap = 2
	cost_modifier = 1.0
	trigger = {{
		capital_scope = {{
			OR = {{
				continent = europe
				continent = mena
				continent = africa
			}}
		}}
		Rights_BUSer3HasGreater = no
		OR = {{
			NOT = {{ stability = 0 }}
			NOT = {{ corruption = 40 }}
			has_any_disaster = no
			NOT = {{ num_of_loans = 3 }}
		}}
		total_development = {MinDev}
		NOT = {{ total_development = {MaxDev} }}
	}}
	# No home province means local mercenary company
}}
""".format(MinDev = MinDev, MaxDev= MaxDev, Scaling=LargeScaling)
	CompanyL += """ merc_dev_{MinDev}_{MaxDev}_small: "Minor free company"
 merc_dev_{MinDev}_{MaxDev}_med: "Local mercenary company"
 merc_dev_{MinDev}_{MaxDev}_large: "Grand mercenary company"
""".format(MinDev = MinDev, MaxDev= MaxDev)
	
file.write(Company)
file2.write(CompanyL)


file.close
file2.close
