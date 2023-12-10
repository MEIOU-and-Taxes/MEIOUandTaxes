import os

# This file reads common/tradenodes/00_tradenodes.txt and map/default.map to generate set of province groups for map/provincegroup.txt consisting of land provinces in trade nodes, and/or adjacent trade nodes, and trade node centers.
# The script result is put in output.txt which is then copied over into the appropriate section of map/provincegroup.txt.

def parse_line(line):
	split_line = line.strip().split('"')
	tokens = []
	for i, split_section in enumerate(split_line):
		if i % 2 == 0:  # If even, so not "
			split_section = split_section.replace("="," = ").replace("{"," { ").replace("}"," } ")
			if "#" in split_section:
				split_section = split_section.split("#")[0]
				tokens.extend(split_section.split())
				return tokens
			tokens.extend(split_section.split())
		else:
			tokens.append('"%s"' % split_section)
	return tokens

def parse_file(fn):
	def update(dic, new):
		if isinstance(new, dict):
			new = new.items()
		for key, val in new:
			if key not in dic:
				dic[key] = val
			elif isinstance(dic[key], list):
				dic[key].append(val)
			else:
				dic[key] = [dic[key], val]
	d = {}
	names = []
	stack = [(d, "")]
	tokens = []
	key = ""
	with open(fn, "rb") as file:
		file = file.read()
		try:
			file = file.decode("utf-8")
		except UnicodeDecodeError:
			file = file.decode("cp1252", errors="ignore")
		for line in file.splitlines():
			tokens += parse_line(line)
		for token in tokens:
			if token == "=":
				key = names.pop()
			elif token == "{":
				dd = {}
				update(stack[-1][0], {key: dd})
				stack.append((dd,key))
				key = ""
			elif token == "}":
				if len(stack[-1][0]):
					update(stack.pop()[0], [(n,n) for n in names])
				else:
					k = stack.pop()[1]
					stack[-1][0][k] = []
					update(stack[-1][0], [(k,n) for n in names])
				names = []
			else:
				names.append(token)
				if key:
					update(stack[-1][0], {key: names.pop()})
					key = ""
	return d

tradenodes_file = parse_file(os.path.join('common', 'tradenodes', '00_tradenodes.txt'))

nodes = dict()

for i, node in enumerate(tradenodes_file):
	nodes[node] = []

for node in tradenodes_file:
	if 'outgoing' in tradenodes_file[node]:
		for link in tradenodes_file[node]['outgoing']:
			if isinstance(link, dict):
				nodes[node].append(link['name'].strip('"'))
				nodes[link['name'].strip('"')].append(node)
			elif link == 'name':
				nodes[node].append(tradenodes_file[node]['outgoing']['name'].strip('"'))
				nodes[tradenodes_file[node]['outgoing']['name'].strip('"')].append(node)



# Create additional link between venezia and genoa nodes
nodes['genoa_node'].append('venezia_node')
nodes['venezia_node'].append('genoa_node')

map_file = parse_file(os.path.join('map', 'default.map'))

centers = 'tradenode_centers = { '
single = ''
multiple = ''

for i, node in enumerate(nodes):
	center = tradenodes_file[node]['location']

	centers += '%s ' % center
	single += 'tradenode_%s = { ' % (i + 1)
	multiple += 'tradenode_mult_%s = { ' % (i + 1)

	for member in tradenodes_file[node]['members']:
		if not member in map_file['sea_starts'] and not member in map_file['lakes']:
			single += '%s ' % member

	for link in nodes[node]:
		for member in tradenodes_file[link]['members']:
			if not member in map_file['sea_starts'] and not member in map_file['lakes']:
				multiple += '%s ' % member

	single += f'}} # {str(node)}\n'
	multiple += f'}} # {str(node)}\n'

centers += '}\n'

with open('output.txt', 'w') as output_file:
	output_file.write(f'{single}\n# Mults are all the provinces in adjacent trade nodes\n{multiple}\n{centers}\n')
