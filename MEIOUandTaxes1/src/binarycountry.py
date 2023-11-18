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

def btree(lst, td, form, body):
    if not len(lst):
        return ''
    elif len(lst) == 1:
        return body % lst[0]
    else:
        return form % (td[lst[int(len(lst)/2)]],
                       btree(lst[int(len(lst)/2):], td, form.replace('\n', '\n\t'), body),
                       btree(lst[:int(len(lst)/2)], td, form.replace('\n', '\n\t'), body))
        
if __name__ == "__main__":
        import glob

        files = glob.glob('common\country_tags\*.txt')
        tags = []

        for file in files:
                tmp = parse_file(file)

                for tag in tmp:
                        tags.append(tag)

        td = { tag:tags.index(tag) + 1 for tag in tags }

        cond = 'check_key = { lhs = $var$ value = %s }'
        body = '%s = { save_event_target_as = $return$ }'
        form = 'if = { limit = { %s }\n\t%s\n}\nelse = {\n\t%s\n}' % (cond, '%s', '%s')

        with open('output.txt', 'w') as f:
                f.write(btree(tags, td, form, body))

        form = '%s = { set_key = { lhs = ID_Tag value = %s } }\n'
        txt = ''

        for tag in tags:
                txt += form % (tag, td[tag])

        with open('outputt.txt', 'w') as f:
                f.write(txt)
