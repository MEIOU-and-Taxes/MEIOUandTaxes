import glob

for file in glob.glob('history\provinces\*.txt'):
    with open(file, encoding='ISO-8859-1') as f:
        t = f.read()
        t = t.replace('POP_ProdDemands', 'Disp_Trade')

        with open(file, 'w', encoding='ISO-8859-1') as ff:
            ff.write(t)
