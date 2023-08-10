import re

file = open('dbz.log', 'r')
text = file.read()
file.close()
list_of_dbz = re.findall(r'(?<=Variable division with zero attempted for variable ")(\w\w\w)', text,
                         flags=re.MULTILINE | re.DOTALL)

dbz_dict = {i: list_of_dbz.count(i) for i in list_of_dbz}
keys = list(dbz_dict.keys())
with open('keys.txt') as rf:
    lines = rf.readlines()
    for line in lines:
        if line.partition(':')[2].strip() in keys:
            dbz_dict[line.partition(':')[0].strip()] = dbz_dict.pop(line.partition(':')[2].strip())

with open('dbz.txt', 'w') as wf:
    for key, count in dbz_dict.items():
        print('Key: {0} attempted division by zero {1} times'.format(key, count), sep='\n', file=wf)

