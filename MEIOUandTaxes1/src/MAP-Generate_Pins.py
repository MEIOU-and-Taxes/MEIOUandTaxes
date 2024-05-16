import re,os

def parse_line(line):
    s = line.strip()
    ss = s.split('"')
    tokens = []
    for i,sss in enumerate(ss):
        if i%2==0:
            sss = sss.replace("="," = ").replace("{"," { ").replace("}"," } ")
            if "#" in sss:
                sss = sss.split("#")[0]
                tokens.extend(sss.split())
                return tokens
            tokens.extend(sss.split())
        else:
            tokens.append('"%s"' % sss)
    return tokens

def parse_file_o(fn):
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
    stack = [(d,"")]
    tokens = []
    key = ""
    with open(fn,"rb") as f:
        ff = f.read()
        fff = ff.decode("iso-8859-1")
        for line in fff.splitlines():
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

def parse_block(block):
	block = re.sub('\#.*\".*?\".*', '', block)
	strings = re.findall('\".*?\"', block)
	block = re.sub('\".*?\"', ' %s ', block)
	block = re.sub('#.*', '\n', block)
	block = re.sub('(\[\[[\w&$]*\]|\^\^[\w&$]*\^|[\>\<\!\=]+|[\{\}\]^])', r' \1 ', block)
	block = block.strip()

	if block:
		block = re.split('\s+', block)

		if strings:
			i = 0

			for ii in range(len(block)):
				if block[ii] == '%s':
					block[ii] = strings[i]

					i += 1

		return block
	else:
		return []

def parse_file(path):
	with open(path, encoding='ISO-8859-1') as f:
		file = list()
		stack = [file]
		rhs = False
	
		for token in parse_block(f.read()):
			if token == '=' or token == '>' or token == '<' or token == '>=' or token == '<=' or token == '==' or token == '!=':
				rhs = True

				stack[-1][-1] = [stack[-1][-1], token]
				stack.append(stack[-1][-1])
			elif token == '{':
				stack[-1].append(list())

				if rhs:
					rhs = False
					
					stack.append(stack.pop()[-1])
				else:
					stack.append(stack[-1][-1])
			elif token == '}' or token == ']' or token == '^':
				stack.pop()
			elif '[[' in token or '^^' in token:
				stack[-1].append([token[1:], list()])
				stack.append(stack[-1][-1][1])
			else:
				stack[-1].append(token)

				if rhs:
					rhs = False

					stack.pop()

		return file
def reconstruct(file, t=''):
	txt = ''

	for f in file:
		if f:
			if len(f) == 3 and type(f[0]) != type(list()) and type(f[1]) != type(list()):
				if type(f[2]) == type(list()):
					txt += '%s%s %s {' % (t, f[0], f[1])

					if not f[2]:
						txt += '}\n'
					elif type(f[2][0]) != type(list()):
						for item in f[2]:
							txt += ' %s' % item
						txt += ' }\n'
					else:
						txt += '\n%s%s}\n' % (reconstruct(f[2], t + '\t'), t)
				else:
					txt += '%s%s %s %s\n' % (t, f[0], f[1], f[2])

	return txt
		  

path = ""

default_map = parse_file_o(os.path.join(path, "map", "default.map"))

provnumber = int(default_map["max_provinces"])

climate = parse_file_o(os.path.join(path, "map", "climate.txt"))


if __name__ == '__main__':
	import glob

	for path in glob.glob('map\\positions.txt'):
		file = parse_file(path)

		for block in file:
			if (str(block[0]) not in default_map["only_used_for_random"] and not str(block[0]) in default_map["lakes"] and not str(block[0]) in climate['impassable']):
				if type(block[2]) == type(list()):
					for entry in block[2]:
						if entry[0] == 'position':
							del (entry[2])[2:]
							entry[2].insert(1, '2.000')
						if entry[0] == 'rotation':
							del (entry[2])[2:]
							entry[2].insert(1, '0.000')
					del (block[2])[2:]
					block[2].insert(0, ['name', '=', f'"pin_{block[0]}"'])
					block[2].insert(1, ['hidden_on_start', '=', 'yes'])
					block[0] = 'object'
			else:
				block.clear()

		with open('map\\pinpos.txt', 'w', encoding='ISO-8859-1') as f:
			f.write(reconstruct(file))