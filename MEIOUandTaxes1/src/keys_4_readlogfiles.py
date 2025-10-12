import os

os.chdir(os.path.dirname(__file__))

files = ('error.log', 'game.log')

def removestuff(file):
    out = ""
    for line in file:
        if line.startswith('[effectimp'):
            out += line
    return out

def convfile(file):
    errorlog = os.path.join(os.path.dirname(__file__), '..','..','..','logs',file)
    outlog = os.path.join(os.path.dirname(__file__), '..','..','..','logs',"CONV_"+file)
    if os.path.isfile(errorlog):
        with open(errorlog, "r") as log, open(outlog, "w") as out:
            y = removestuff(log)
            for x in variables.variables():
                y = y.replace(x, variables[x])
            out.write(y)
    else:
        print('Could not find file')

with open("keys.txt", "r") as variablefile:
    variables = {}
    for variable in variablefile:
        variable = variable.strip("\n").split(":")
        variables["\""+variable[1].strip(" ")+"\""] = variable[0].strip(" ")

for file in files:
    print('Converting '+str(file)+'...')
    convfile(file)
    print('Wrote to CONV_'+str(file))
print('Done!')
input()