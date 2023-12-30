import glob

if __name__ == "__main__":
    clean = []

    with open("common\\buildings\\04_legacy_buildings.txt") as f:
        for line in f.readlines():
            if line[0].isalpha():
                clean.append(line.split(' ')[0])

    clean.remove("small_university")
    clean.remove("medium_university")

    for prov in glob.glob("history\\provinces\\*.txt"):
        with open(prov) as f:
            t = f.read()

            for building in clean:
                t = t.replace("\n%s " % building, "\n#%s " % building)
                t = t.replace("\t%s " % building, "\t#%s " % building)
                t = t.replace(" %s " % building, " #%s " % building)

            with open(prov, 'w') as ff:
                ff.write(t)
