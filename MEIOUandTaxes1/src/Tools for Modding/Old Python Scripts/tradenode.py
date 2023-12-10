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
	stack = [(d,"")]
	tokens = []
	key = ""
	with open(fn,"rb") as f:
		ff = f.read()
		try:
			fff = ff.decode("utf-8")
		except UnicodeDecodeError:
			fff = ff.decode("cp1252", errors="ignore")
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

def lst_t_str(lst):
    tmpstr = ''

    for i in lst:
        tmpstr += str(i) + ' '

    return tmpstr

def get_tradenode_group(fn, fnn):
    f = parse_file(fn)
    ff = parse_file(fnn)
    
    tradenode_centers = "tradenode_centers = {\n\t"
    tradenodes = ""
    tradenodes_tmplt = "%s = {\n\t%s\n}\n"
    effect = ""
    effect_tmplt = "\t%s = { set_variable = { which = TN_Link%s value = %s } }\n"

    ii = 1
    
    for tn in f:
        f[tn]['members'] = [i for i in f[tn]['members'] if (i not in ff["sea_starts"]) and (i not in ff["lakes"])]
        
        tradenode_centers += str(f[tn]['location']) + ' '
        tradenodes += tradenodes_tmplt % ('tradenode_%d' % ii, lst_t_str(f[tn]['members']))

        ii += 1

        if 'outgoing' in f[tn]:
            if type(f[tn]['outgoing']) == type([]):
                i = 0
                
                for og in f[tn]['outgoing']:
                    effect += effect_tmplt % (f[tn]['location'], str(i), f[og['name'].replace('"', '')]['location'])
                    
                    i += 1
            else:
                effect += effect_tmplt % (f[tn]['location'], '0', f[f[tn]['outgoing']['name'].replace('"', '')]['location'])

    tradenode_centers += '\n}\n'

    with open('output.txt', 'w') as ff:
        ff.write(tradenodes + '\n\n' + tradenode_centers + '\n\n' + effect)

if __name__ == '__main__':
	get_tradenode_group('common\\tradenodes\\00_tradenodes.txt', 'map\\default.map')
