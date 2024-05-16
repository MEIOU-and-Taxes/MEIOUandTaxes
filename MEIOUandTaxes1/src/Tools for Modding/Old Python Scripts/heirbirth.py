# -*- coding: utf-8 -*-
"""
Created on Sat May  2 09:19:09 2020

@author: vinef
"""

import os 
import codecs
import re
from datetime import datetime
import pandas as pd

class Tag():
	def __init__(self,tag,heir,birthday,name,dynasty,monarch):
		self.tag = tag
		self.heir = heir
		self.birthday = birthday
		self.name = name 
		self.dynasty = dynasty
		self.monarch = monarch
		tags.append(self)

tags = []

for file in os.listdir(os.getcwd()+r'\history\countries'):
	if file.endswith('.txt'):
		filepath = os.getcwd()+r'\history\countries\\'+file
		fileobj = codecs.open(filepath, 'r', encoding='latin-1')
		contents = fileobj.read()
		heirs = re.findall(r'(\s*heir\s*=\s*\{.*?\})|(define_heir\s*=\s*\{.*?\})',contents,flags=re.DOTALL|re.IGNORECASE) #
		if heirs:
			heirdict = {}
			for heir in heirs:
				heir = heir[0]
				birthday = re.findall(r'birth_date\s*=\s*([''"".\d]+)', heir,flags=re.IGNORECASE)
				if birthday:
					birthday = re.sub(r'[^.\d]','',birthday[0])
					birthday = datetime.strptime(birthday,'%Y.%m.%d')
				if not birthday:
					pattern = r'(\d\d\d\d\.\d?\d\.\d?\d)(?:\s*=\s*{{.*?){}'.format(re.escape(heir))
					birthdays = re.findall(pattern, contents,flags=re.IGNORECASE|re.DOTALL)
					birthdays = [datetime.strptime(birthday, '%Y.%m.%d') for birthday in birthdays if datetime.strptime(birthday, '%Y.%m.%d') < datetime(1356,12,26)]
					birthday = max(birthdays)
				if birthday < datetime(1356,12,26):
					heirdict[birthday] = heir
			for heir in heirdict.items():
				if heir[0] == max(heirdict.keys()):
					Tag(file[0:3],heir[1],heir[0])
					break

tagsforframe = [tag.tag for tag in tags]
birthdates = [tag.birthday for tag in tags ]
birthdaysforframe = [(birthdate - min(birthdates)).days for birthdate in birthdates]	
heirframedict = {'Tag':tagsforframe,'Birthdate':birthdaysforframe}
heirframe = pd.DataFrame(heirframedict)
heirframe.to_csv('heirs.csv',index=False)	
					
				
					
		#print(heirs)