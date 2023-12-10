import os

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

def btree(lst, form, body):
    if not len(lst):
        return ''
    elif len(lst) == 1:
        return body % lst[0]
    else:
        return form % (lst[int(len(lst)/2)],
                       btree(lst[int(len(lst)/2):], form.replace('\n', '\n\t'), body),
                       btree(lst[:int(len(lst)/2)], form.replace('\n', '\n\t'), body))
        
if __name__ == "__main__":
        tlrnc = [i for i in range(1, 13)]

        cond = 'check_variable = { which = Growth_OutClass value = %s }'
        body = 'multiply_variable = { which = Growth_Pref which = %s }'
        form = 'if = {\n\tlimit = {\n\t\t%s\n\t}\n\t%s\n}\nelse = {\n\t%s\n}' % (cond, '%s', '%s')

        with open('output.txt', 'w') as f:
                f.write(btree(tlrnc, form, body))
        
        """
        path = 'map'
        default_map = parse_file(os.path.join(path, "default.map"))
        climate = parse_file(os.path.join(path, "climate.txt"))
        land = [prov for prov in range(int(default_map['max_provinces']) + 1)[1:]
                if not(str(prov) in default_map['sea_starts'])
                and not(str(prov) in default_map['only_used_for_random'])
                and not(str(prov) in default_map['lakes'])
                and not(str(prov) in climate['impassable'])]
        t = 'every_province_land = {\n\t'

        for prov in land:
                t += '{} '.format(str(prov))

        t += '\n}\n'

        with open('output.txt', 'w') as f:
                f.write(t)
        """
    
        """

        cond = 'check_key = { lhs = S_ID value = %s }'
        body = '%s = { save_event_target_as = GetProvOut }'
        form = 'if = {\n\tlimit = {\n\t\t%s\n\t}\n\t%s\n}\nelse = {\n\t%s\n}' % (cond, '%s', '%s')

        with open('output.txt', 'w') as f:
                f.write(btree(land, form, body))
        """

