# -*- coding: utf-8 -*-
"""
Created on Sat May  2 09:19:09 2020

@author: vinef
"""

import os 
import codecs
import re
from datetime import datetime

class event():
	def __init__(self, inbody, type):
		self.inbody = inbody
		if type == 'year':
			try: #fun fact, for some reason you *must* zero pad the year in the below function, but you don't have to zeropad anything else
				self.date = datetime.strptime(re.findall('^\s*\d{1,}\.\d?\d\.\d?\d', self.inbody)[0], '%Y.%m.%d')
			except:
				self.date = datetime(1000,1,1)
		elif type == 'relation':
			try: 
				self.date = datetime.strptime(re.findall('(?:start_date\s*=\s*)(\d{1,}\.\d?\d\.\d?\d)', self.inbody)[0], '%Y.%m.%d')
			except:
				self.date = datetime(1000,1,1) #if it breaks its very likely because the year is below 1000
		if self.date > datetime(1356,12,31):
			self.outbody = re.sub('#$', '', re.sub('^','#', self.inbody, flags=re.M))
		else:
			self.outbody = self.inbody

for file in os.listdir(os.getcwd()+r'\history\countries'):
	if file.endswith('.txt'):
		filepath = os.getcwd()+r'\history\countries\\'+file
		fileobj = codecs.open(filepath, 'r', encoding='latin-1')
		contents = fileobj.read()
		fileobj.close()
		years = re.split(r'(^)(?=\s*\d{1,}\.\d?\d\.\d?\d\s*=\s*\{)', contents, flags=re.M)
		years = [event(year, 'year') for year in years if re.match('^\s*\d{1,}\.\d?\d\.\d?\d', year)]
		for year in years:
			contents = re.sub(re.escape(year.inbody),year.outbody, contents)
		fileobj = codecs.open(filepath, 'w+', encoding='latin-1')
		fileobj.write(contents)
		fileobj.close()
		
for file in os.listdir(os.getcwd()+r'\history\provinces'):
	if file.endswith('.txt'):
		filepath = os.getcwd()+r'\history\provinces\\'+file
		fileobj = codecs.open(filepath, 'r', encoding='latin-1')
		contents = fileobj.read()
		fileobj.close()
		years = re.split(r'(^)(?=\s*\d{1,}.\d?\d\.\d?\d\s*=\s*\{)', contents, flags=re.M)
		years = [event(year, 'year') for year in years if re.match('^\s*\d{1,}\.\d?\d\.\d?\d', year)]
		for year in years:
			contents = re.sub(re.escape(year.inbody),year.outbody, contents)
		fileobj = codecs.open(filepath, 'w+', encoding='latin-1')
		fileobj.write(contents)
		fileobj.close()
			
			
for file in os.listdir(os.getcwd()+r'\history\diplomacy'):
	if file.endswith('.txt'):
		filepath = os.getcwd()+r'\history\diplomacy\\'+file
		fileobj = codecs.open(filepath, 'r', encoding='latin-1')
		contents = fileobj.read()
		fileobj.close()
		relations = re.split(r'(^)(?=\s*\w+\s*=\s*\{)', contents, flags=re.M)
		relations = [event(relation, 'relation') for relation in relations if re.match('^\s*\w+\s*=\s*\{', relation)]
		for relation in relations:
			contents = re.sub(re.escape(relation.inbody),relation.outbody, contents)
		fileobj = codecs.open(filepath, 'w+', encoding='latin-1')
		fileobj.write(contents)
		fileobj.close()