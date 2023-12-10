import codecs
from os import read
import pandas as pd
import numpy as np


provinces_map = pd.read_csv('map/definition.csv', sep=';', encoding='utf-8-sig')

provinces_input = pd.read_csv('map/RNW_ProvinceID_List.csv', sep=';')

for index, row in provinces_map.iterrows():
    if(len(provinces_input[provinces_input['Id'] == row.province])) == 0:
        row.x = 'x'

provinces_map.to_csv('map/definition.csv', sep=';',index=False, header=True, encoding='utf-8-sig')