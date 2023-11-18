# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:53:38 2020

@author: ellis jones #don't dox me pls
"""

import re

file = open('error.log', 'r')
text = file.read()
file.close()
text = re.sub(r'\[virtualfilesystem_physfs\.cpp:\d+\]: Could not open file:[^\[]*', '', text)
text = re.sub(r'\[virtualfilesystem\.cpp:\d+\]: Failed to find[^\[]*', '', text)
text = re.sub(r'\[virtualfilesystem\.cpp:\d+\]: Invalid file when updating checksum:[^\[]*', '', text)
text = re.sub(r'\[version\.cpp:\d+\]: Invalid file when updating checksum:[^\[]*', '', text)
text = re.sub(r'\[province\.cpp:\d+\]: _Discovered capacity should be at least[^\[]*', '', text)
text = re.sub(r'\[trigger\.cpp:\d+\]: Error "failed trigger validation for[^\[]*', '', text)
text = re.sub(r'\[pdx_entity\.cpp:\d+\]: Entity state not found.[^\[]*', '', text)
text = re.sub(r'\[graphics\.cpp:\d+\]: No font with name[^\[]*', '', text)
text = re.sub(r'\[country_cached_data\.cpp:\d+\]:[^\[]*', '', text)
text = re.sub(r'\[triggerimplementation\.cpp:\d+\]: Trigger error: \[triggerimplementation\.cpp:\d+\]:[^\[]*[triggerimplementation\.cpp:\d+\]: Root country: [A-Za-z]+ Root province: 0[^\[]*', '', text)
file = open('error.log', 'w+')
file.write(text)
file.close()
