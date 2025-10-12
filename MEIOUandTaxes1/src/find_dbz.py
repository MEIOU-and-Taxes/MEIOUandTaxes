import re

file = open('dbz.log', 'r')
text = file.read()
file.close()
list_of_dbz = re.findall(r'(?<=Variable division with zero attempted for variable ")(\w\w\w)', text,
                         flags=re.MULTILINE | re.DOTALL)

dbz_dict = {i: list_of_dbz.count(i) for i in list_of_dbz}
variables = list(dbz_dict.variables())
with open('variables.txt') as rf:
    lines = rf.readlines()
    for line in lines:
        if line.partition(':')[2].strip() in variables:
            dbz_dict[line.partition(':')[0].strip()] = dbz_dict.pop(line.partition(':')[2].strip())

with open('dbz.txt', 'w') as wf:
    for variable, count in dbz_dict.items():
        print('variable: {0} attempted division by zero {1} times'.format(variable, count), sep='\n', file=wf)

