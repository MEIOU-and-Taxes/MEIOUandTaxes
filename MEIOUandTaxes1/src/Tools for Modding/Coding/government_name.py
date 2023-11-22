# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 09:25:56 2020

@author: vinef
"""

import re
import codecs

file = codecs.open('government_names_output.txt', 'w+', encoding = 'latin-1')
government_names = []
class GovernmentName:
    name = 'default'
    rank_1_m = 'COUNT'
    rank_1_f = 'COUNTESS'
    rank_2_m = 'MARGRAVE'
    rank_2_f = 'MARGRAVINE'
    rank_3_m = 'DUKE'
    rank_3_f = 'DUCHESS'
    rank_4_m = 'PRINCE'
    rank_4_f = 'PRINCESS'
    rank_5_m = 'KING',
    rank_5_f = 'QUEEN'
    rank_6_m = 'EMPEROR'
    rank_6_f = 'EMPRESS'
    heir_m = 'CROWN_PRINCE'
    heir_f = 'CROWN_PRINCESS'
    def __init__(self,name,culture,rank_1_m,rank_1_f,rank_2_m,rank_2_f,rank_3_m ,rank_3_f,rank_4_m,rank_4_f,rank_5_m,rank_5_f,rank_6_m,rank_6_f, heir_m, heir_f):
        self.name = name
        self.culture = culture
        self.rank_1_m = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_1_m.upper().replace(' ', '_')))
        self.rank_1_f = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_1_f.upper().replace(' ', '_')))
        self.rank_2_m = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_2_m.upper().replace(' ', '_')))
        self.rank_2_f = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_2_f.upper().replace(' ', '_')))
        self.rank_3_m = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_3_m.upper().replace(' ', '_')))
        self.rank_3_f = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_3_f.upper().replace(' ', '_')))
        self.rank_4_m = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_4_m.upper().replace(' ', '_')))
        self.rank_4_f = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_4_f.upper().replace(' ', '_')))
        self.rank_5_m = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_5_m.upper().replace(' ', '_')))
        self.rank_5_f = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_5_f .upper().replace(' ', '_')))
        self.rank_6_m = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_6_m.upper().replace(' ', '_')))
        self.rank_6_f = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', rank_6_f .upper().replace(' ', '_')))
        self.heir_m = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', heir_m.upper().replace(' ', '_')))
        self.heir_f = re.sub('^(...)$', r'\1_title', re.sub('^(...)_TITLE$', r'\1_title', heir_f.upper().replace(' ', '_')))
        government_names.append(self)
            
lithuanian = GovernmentName(name='lithuanian',culture='OR = {\n\t\t\tprimary_culture = lithuanian\n\t\t\tprimary_culture = old_prussian\n\t\t}', rank_1_m = 'GRAFAS', rank_1_f = 'GRAFIENE', rank_2_m = 'MARKIZAS', rank_2_f = 'MARKIZIENE', rank_3_m = 'HERCOGas', rank_3_f = 'HERCOGIENE', rank_4_m = 'PRINCAS', rank_4_f = 'PRINCESE', rank_5_m = 'KARALIUS', rank_5_f = 'KARALIENE', rank_6_m = 'IMPERATORIUS', rank_6_f = 'IMPERATORIENE', heir_m = 'KARUNOS_PRINCAS', heir_f = 'KARUNOS_PRINCESE')
danish = GovernmentName('danish', 'primary_culture = danish', 'Greve', 'Grevinde', 'Markis', 'Markise', 'Hertug', 'Hertuginde', 'Fyrste', 'Fyrste', 'konge','dronning', 'kejser','kejserinde','kronprins','kronprinsesse')
swedish = GovernmentName('swedish', 'primary_culture = swedish', 'Greve', 'grevinna', 'Markis', 'Markisinna', 'Hertig', 'Hertiginna', 'Furste', 'Furstinna', 'kung','drottning', 'kejsare','kejsarinna','kronprins','kronprinsessa')
norwegian = GovernmentName('norwegian', 'primary_culture = norwegian', 'Jarl', 'Grevinne', 'Marki', 'Markise', 'Hertug', 'Hertuginne', 'Fyrste', 'Fyrstinne', 'konge','dronning', 'keiser','keiserinne','kronprins','kronprinsesse')
latvian = GovernmentName('latvian', 'OR = {\n\t\t\tprimary_culture = latvian\n\t\t\tprimary_culture = lattgalian\n\t\t\tprimary_culture = curonian\n\t\t}', 'grafs', 'Grafiene', 'Markgrafs', 'Markgrafiene', 'Hercogs', 'Hercogiene', 'Princis', 'Princese', 'Karalis','Karaliene', 'Keizars','keizariene','kronprincis','krona princese')
norse = GovernmentName('norse', 'primary_culture = norse', 'Jarl', 'jarlkona', 'markgreifi', 'markgreifynja', 'hertogi', 'hertogaynja', 'fursti', 'furstynja', 'konungur','drottning', 'keisari','keisarynja','kronprins','kronprinsessa') 
slovak = GovernmentName('slovak', 'primary_culture = slovak', 'Grof', 'grofica', 'markiz', 'markiza', 'vojvoda', 'vojvodkyna', 'princ', 'princeza', 'kral','kralovna', 'cisar','cisarovna','princ','princeza')
georgian = GovernmentName('georgian', 'culture_group = georgian_group', 'Tavadi', 'grapinia', 'margavi', 'margavini', 'hertsogi', 'duksi', 'print', 'printsesa', 'mepe','dedopali', 'imperatori','imperatori','print','printsesa')
breton = GovernmentName('breton', 'OR = {\n\t\t\tprimary_culture = breton\n\t\t\tprimary_culture = cornish\n\t\t}', 'Kont', 'kontez', 'markiz', 'markizez', 'dug', 'dugez', 'prins', 'prinsez', 'roue','rouanez', 'impalaer','impalaerez','prins-her','prinsez-her')
highland_scottish = GovernmentName('highland_scottish', 'primary_culture = highland_scottish', 'cunnt', 'ban-cunnt', 'iarl', 'ban-iarla', 'diuc', 'ban-diuc', 'prionnsa', 'bana-phrionnsa', 'righ','banrigh', 'impire','impireachd','tanaiste','tanaiste')   
basque = GovernmentName('basque', 'primary_culture = basque', 'konde', 'kondesa', 'margrave', 'margravine', 'dukeak', 'dukesa', 'printze', 'printzesa', 'errege','erregina', 'enperadorea','enperatriz','koroaren printzea','koroa printzesa')   



for entry in government_names:
    file.write("""{NAME}_monarchy_title_1 = {{
	rank = {{
		1 = COUNTY
		2 = COUNTY
		3 = COUNTY
		4 = COUNTY
		5 = COUNTY
		6 = COUNTY
        }}
	
	ruler_male = {{
		1 = {COUNT}
		2 = {COUNT}
		3 = {COUNT}
		4 = {COUNT}
		5 = {COUNT}
		6 = {COUNT}
	}}
	
	ruler_female = {{
		1 = {COUNTESS}
		2 = {COUNTESS}
		3 = {COUNTESS}
		4 = {COUNTESS}
		5 = {COUNTESS}
		6 = {COUNTESS}
	}}

	consort_male = {{
		1 = {COUNT}
		2 = {COUNT}
		3 = {COUNT}
		4 = {COUNT}
		5 = {COUNT}
		6 = {COUNT}
	}}
	
	consort_female = {{
		1 = {COUNTESS}
		2 = {COUNTESS}
		3 = {COUNTESS}
		4 = {COUNTESS}
		5 = {COUNTESS}
		6 = {COUNTESS}
	}}
	
	
	heir_male = {{
		1 = HEIR
		2 = HEIR
		3 = HEIR
		4 = HEIR
		5 = HEIR
		6 = HEIR
	}}
	
	heir_female = {{
		1 = HEIR
		2 = HEIR
		3 = HEIR
		4 = HEIR
		5 = HEIR
		6 = HEIR
	}}

	
	trigger = {{
		government = monarchy
		{PRIMARY_CULTURE}
		title_trigger = {{ rank = 1 }}
	}}
}}

{NAME}_monarchy_title_2 = {{
	rank = {{
		1 = MARGRAVIATE
		2 = MARGRAVIATE
		3 = MARGRAVIATE
		4 = MARGRAVIATE
		5 = MARGRAVIATE
		6 = MARGRAVIATE
	}}
	
	ruler_male = {{
		1 = {MARGRAVE}
		2 = {MARGRAVE}
		3 = {MARGRAVE}
		4 = {MARGRAVE}
		5 = {MARGRAVE}
		6 = {MARGRAVE}
	}}
	
	ruler_female = {{
		1 = {MARGRAVINE}
		2 = {MARGRAVINE}
		3 = {MARGRAVINE}
		4 = {MARGRAVINE}
		5 = {MARGRAVINE}
		6 = {MARGRAVINE}
	}}

	consort_male = {{
		1 = {MARGRAVE}
		2 = {MARGRAVE}
		3 = {MARGRAVE}
		4 = {MARGRAVE}
		5 = {MARGRAVE}
		6 = {MARGRAVE}
	}}
	
	consort_female = {{
		1 = {MARGRAVINE}
		2 = {MARGRAVINE}
		3 = {MARGRAVINE}
		4 = {MARGRAVINE}
		5 = {MARGRAVINE}
		6 = {MARGRAVINE}
	}}
	
	
	heir_male = {{
		1 = HEIR
		2 = HEIR
		3 = HEIR
		4 = HEIR
		5 = HEIR
		6 = HEIR
	}}
	
	heir_female = {{
		1 = HEIR
		2 = HEIR
		3 = HEIR
		4 = HEIR
		5 = HEIR
		6 = HEIR
	}}

	
	trigger = {{
		government = monarchy
		{PRIMARY_CULTURE}
		title_trigger = {{ rank = 2 }}
	}}
}}

{NAME}_monarchy_title_3 = {{
	rank = {{
		1 = DUCHY
		2 = DUCHY
		3 = DUCHY
		4 = DUCHY
		5 = DUCHY
		6 = DUCHY
	}}
	
	ruler_male = {{
		1 = {DUKE}
		2 = {DUKE}
		3 = {DUKE}
		4 = {DUKE}
		5 = {DUKE}
		6 = {DUKE}
	}}
	
	ruler_female = {{
		1 = {DUCHESS}
		2 = {DUCHESS}
		3 = {DUCHESS}
		4 = {DUCHESS}
		5 = {DUCHESS}
		6 = {DUCHESS}
	}}

	consort_male = {{
		1 = {DUKE}
		2 = {DUKE}
		3 = {DUKE}
		4 = {DUKE}
		5 = {DUKE}
		6 = {DUKE}
	}}
	
	consort_female = {{
		1 = {DUCHESS}
		2 = {DUCHESS}
		3 = {DUCHESS}
		4 = {DUCHESS}
		5 = {DUCHESS}
		6 = {DUCHESS}
	}}
	
	
	heir_male = {{
		1 = HEIR
		2 = HEIR
		3 = HEIR
		4 = HEIR
		5 = HEIR
		6 = HEIR
	}}
	
	heir_female = {{
		1 = HEIR
		2 = HEIR
		3 = HEIR
		4 = HEIR
		5 = HEIR
		6 = HEIR
	}}

	
	trigger = {{
		government = monarchy
		{PRIMARY_CULTURE}
		title_trigger = {{ rank = 3 }}
	}}
}}

{NAME}_monarchy_title_4 = {{
	rank = {{
		1 = PRINCIPALITY
		2 = PRINCIPALITY
		3 = PRINCIPALITY
		4 = PRINCIPALITY
		5 = PRINCIPALITY
		6 = PRINCIPALITY
	}}
	
	ruler_male = {{
		1 = {PRINCE}
		2 = {PRINCE}
		3 = {PRINCE}
		4 = {PRINCE}
		5 = {PRINCE}
		6 = {PRINCE}
	}}
	
	ruler_female = {{
		1 = {PRINCESS}
		2 = {PRINCESS}
		3 = {PRINCESS}
		4 = {PRINCESS}
		5 = {PRINCESS}
		6 = {PRINCESS}
	}}

	consort_male = {{
		1 = {PRINCE}
		2 = {PRINCE}
		3 = {PRINCE}
		4 = {PRINCE}
		5 = {PRINCE}
		6 = {PRINCE}
	}}
	
	consort_female = {{
		1 = {PRINCESS}
		2 = {PRINCESS}
		3 = {PRINCESS}
		4 = {PRINCESS}
		5 = {PRINCESS}
		6 = {PRINCESS}
	}}
	
	heir_male = {{
		1 = HEIR
		2 = HEIR
		3 = HEIR
		4 = HEIR
		5 = HEIR
		6 = HEIR
	}}
	
	heir_female = {{
		1 = HEIR
		2 = HEIR
		3 = HEIR
		4 = HEIR
		5 = HEIR
		6 = HEIR
	}}

	
	trigger = {{
		government = monarchy
        {PRIMARY_CULTURE}
		title_trigger = {{ rank = 4 }}
	}}
}}

{NAME}_monarchy_title_5 = {{
	rank = {{
		1 = KINGDOM
		2 = KINGDOM
		3 = KINGDOM
		4 = KINGDOM
		5 = KINGDOM
		6 = KINGDOM
	}}
	
	ruler_male = {{
		1 = {KING}
		2 = {KING}
		3 = {KING}
		4 = {KING}
		5 = {KING}
		6 = {KING}
	}}
	
	ruler_female = {{
		1 = {QUEEN}
		2 = {QUEEN}
		3 = {QUEEN}
		4 = {QUEEN}
		5 = {QUEEN}
		6 = {QUEEN}
	}}

	consort_male = {{
		1 = {KING}	
		2 = {KING}
		3 = {KING}
		4 = {KING}
		5 = {KING}
		6 = {KING}
	}}
	
	consort_female = {{
		1 = {QUEEN}
		2 = {QUEEN}
		3 = {QUEEN}
		4 = {QUEEN}
		5 = {QUEEN}
		6 = {QUEEN}
	}}
	
	heir_male = {{
		1 = {CROWN_PRINCE}
		2 = {CROWN_PRINCE}
		3 = {CROWN_PRINCE}
		4 = {CROWN_PRINCE}
		5 = {CROWN_PRINCE}
		6 = {CROWN_PRINCE}
	}}
	
	heir_female = {{
		1 = {CROWN_PRINCESS}
		2 = {CROWN_PRINCESS}
		3 = {CROWN_PRINCESS}
		4 = {CROWN_PRINCESS}
		5 = {CROWN_PRINCESS}
		6 = {CROWN_PRINCESS}
	}}

	trigger = {{
		government = monarchy
		{PRIMARY_CULTURE}
		title_trigger = {{ rank = 5 }}
	}}
}}

{NAME}_monarchy_title_6 = {{
	rank = {{
		1 = EMPIRE
		2 = EMPIRE
		3 = EMPIRE
		4 = EMPIRE
		5 = EMPIRE
		6 = EMPIRE
	}}
	
	ruler_male = {{
		1 = {EMPEROR}
		2 = {EMPEROR}
		3 = {EMPEROR}
		4 = {EMPEROR}
		5 = {EMPEROR}
		6 = {EMPEROR}
	}}
	
	ruler_female = {{
		1 = {EMPRESS}
		2 = {EMPRESS}
		3 = {EMPRESS}
		4 = {EMPRESS}
		5 = {EMPRESS}
		6 = {EMPRESS}
	}}

	consort_male = {{
		1 = {EMPEROR}
		2 = {EMPEROR}
		3 = {EMPEROR}
		4 = {EMPEROR}
		5 = {EMPEROR}
		6 = {EMPEROR}
	}}
	
	consort_female = {{
		1 = {EMPRESS}
		2 = {EMPRESS}
		3 = {EMPRESS}
		4 = {EMPRESS}
		5 = {EMPRESS}
		6 = {EMPRESS}
	}}
	
	heir_male = {{
		1 = {CROWN_PRINCE}
		2 = {CROWN_PRINCE}
		3 = {CROWN_PRINCE}
		4 = {CROWN_PRINCE}
		5 = {CROWN_PRINCE}
		6 = {CROWN_PRINCE}
	}}
	
	heir_female = {{
		1 = {CROWN_PRINCESS}
		2 = {CROWN_PRINCESS}
		3 = {CROWN_PRINCESS}
		4 = {CROWN_PRINCESS}
		5 = {CROWN_PRINCESS}
		6 = {CROWN_PRINCESS}
	}}

	
	trigger = {{
		government = monarchy
		{PRIMARY_CULTURE}
		title_trigger = {{ rank = 6 }}
	}}
}}

""".format(PRIMARY_CULTURE=entry.culture,NAME=entry.name,COUNT=entry.rank_1_m,COUNTESS=entry.rank_1_f,MARGRAVE=entry.rank_2_m,MARGRAVINE=entry.rank_2_f,DUKE=entry.rank_3_m,DUCHESS=entry.rank_3_f,PRINCE=entry.rank_4_m,PRINCESS=entry.rank_4_f,KING=entry.rank_5_m,QUEEN=entry.rank_5_f,EMPEROR=entry.rank_6_m,EMPRESS=entry.rank_6_f,CROWN_PRINCE=entry.heir_m,CROWN_PRINCESS=entry.heir_f))

file.close()