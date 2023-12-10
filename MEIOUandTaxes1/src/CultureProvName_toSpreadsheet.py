import os
import re
re_comment = re.compile(r"#.*")

def parse_into_spreadsheet(output):
	ospath = os.path.join(os.getcwd(), "common", "province_names")
	provdata = dict()
	data = dict()
	with open(os.path.join(os.getcwd(), "map", "definition.csv"), "r") as provs:
		for prov in provs:
			prov = prov.split(";")
			try:
				num = int(prov[0])
			except:
				num = 0
			provdata[str(num)] = prov[4].rstrip("\n")

	paths = [os.path.join(ospath, f) for f in os.listdir(ospath) if os.path.isfile(os.path.join(ospath, f))]
	for path in paths:
		content = dict()
		with open(path, "r", encoding = 'cp1252') as text:
			for line in text:
				line = re.sub(re_comment, "", line.rstrip("\n"))
				if line != "":
					line = line.split("=")
					content[line[0].strip(" ")] = line[1].strip(" ").strip("\"")
		data[os.path.basename(path).rstrip(".txt")] = content

	with open(output, "w", encoding = 'cp1252') as out:
		out.write("Province IDs;")
		for x in provdata:
			out.write(x + ";")
		out.write("\nDefault;")
		for x in provdata:
			out.write(provdata[x] + ";")
		for x in data:
			out.write("\n" + x + ";")
			for y in provdata:
				if y in data[x]:
					out.write(data[x][y] + ";")
				else:
					out.write(";")


if __name__ == "__main__":
	filepath = os.path.join(os.getcwd(), "ProvinceCultureNames.txt")

	parse_into_spreadsheet(filepath)
