# This script reads all the variables from events/00-Province_Setup and outputs them to provs_setup.csv for easy reading/use

import sys, os
import csv
from pathlib import Path
import re

# Read in the input
input_file = Path('events/00-Province_Setup.txt')
input = input_file.read_text()

# Setup and use the regexes to scan the which and value for every variable
val_which_regex = re.compile(r'(?<=which = )\w+')
val_value_regex = re.compile(r'(?<=value =)\s+[0-9.]+')
which_matches = val_which_regex.findall(input)
value_matches = val_value_regex.findall(input)

# Open the output csv
with open(Path('provs_setup.csv'), 'w', encoding='utf-8') as out:

    # Write the Header
    out.write(which_matches[0]+',')
    max_columns = 1
    for match in which_matches[1:]:
        if match == which_matches[0]:
            break
        else:
            out.write(match+',')
            max_columns +=1
    out.write('\n')

    # Write the data
    column = 0
    for match in value_matches:
        out.write(match.strip() + ',')
        column += 1
        if column == max_columns:
            out.write('\n')
            column = 0