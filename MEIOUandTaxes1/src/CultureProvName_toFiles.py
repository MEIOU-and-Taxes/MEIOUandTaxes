import os

def write_files(inpt):
	data = dict()
	with open(inpt, "r") as inp:
		ospath = os.path.join(os.getcwd(), "common", "province_names")
		for line in inp:
			line = line.rstrip("\n").split(";")
			data[line[0]] = line[1:]
	provinces = data.pop("Province IDs")
	if "Default" in data:
		del data["Default"]
	for culturelist in data:
		with open(os.path.join(ospath, culturelist + ".txt"), "w") as out:
			for prov, x in enumerate(data[culturelist][1:], 1):
				if x != "":
					out.write(provinces[prov] + " = \"" + x + "\"\n")




if __name__ == "__main__":
	filepath = os.path.join(os.getcwd(), "ProvinceCultureNames.txt")
	write_files(filepath)
