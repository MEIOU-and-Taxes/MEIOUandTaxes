import glob
import os
import re

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

def get_prov(idp, t):
	match = re.search(rf'\n-{idp}={{(.*?)\n\t}}', t, re.DOTALL)
	return match.group(1) if match else ''

def get_country(tag, t):
	match = re.search(rf'\t}}\n\t{tag}={{(.*?)\n\t}}', t, re.DOTALL)
	return match.group(1) if match else ''

def get_var(t):
	match = re.search(r'\tvariables={(.*?)}', t, re.DOTALL)
	return match.group(1).strip().replace('\t', '') if match else 'clz=0.000'

def get_flag(t):
	match = re.search(r'\tflags={(.*?)}', t, re.DOTALL)
	return match.group(1).strip().replace('\t', '') if match else 'foo=1356.1.1'

def get_modifier(t):
	out = []

	for match in re.finditer(r'\t\tmodifier={(.*?)}', t, re.DOTALL):
		block = match.group(1)
		
		if '\tpermanent=yes\n' in block:
			tstr = '_ppm'
		else:
			tstr = '_pm'

		if '\thidden=yes\n' in block:
			tstr += 'h'

		tstr += '={m=%s}' % re.search(r'"(.*?)"', block).group(1)

		out.append(tstr)

	return out

def get_modifier2(t):
	out = []

	for match in re.finditer(r'\t\tmodifier={(.*?)}', t, re.DOTALL):
		block = match.group(1)
		
		if '\thidden=yes\n' in block:
			tstr = '_cmh'
		else:
			tstr = '_cm'

		tstr += '={m=%s}' % re.search(r'"(.*?)"', block).group(1)

		out.append(tstr)

	return out

def get_history(prov, var, flag, modifier):
	#if not prov or not var or not flag or not modifier:
	#	print(f"Missing input data in get_history: prov={prov}, var={var}, flag={flag}, modifier={modifier}")
	
	out = '%s = {\n' % prov
	var_out = []
	flag_out = []
	modifier_out = []

	for v in var:
		v = v.split('=')
		if len(v) > 1 and  v[1] != '0.000':
			var_out.append('_v={v=%s n=%s} ' % (v[0], v[1]))

	for f in flag:
		if len(f) > 0:
			flag_out.append('_pf={f=%s} ' % f)
			
	for m in modifier:
		modifier_out.append('%s ' % m)

	out += ''.join(var_out) + '\n' + ''.join(flag_out) + '\n' + ' '.join(modifier_out) + '}\n'

	return out

def get_history2(tag, var, flag, modifier):
	if not tag or not var or not flag or not modifier:
		print(f"Missing input data in get_history2: tag={tag}, var={var}, flag={flag}, modifier={modifier}")
	out = '%s = {\n' % tag
	var_out = []
	flag_out = []
	modifier_out = []

	for v in var:
		v = v.split('=')
		if len(v) > 1 and  v[1] != '0.000':
			var_out.append('_v={v=%s n=%s} ' % (v[0], v[1]))

	for f in flag:
		if len(f) > 0:
			flag_out.append('_cf={f=%s} ' % f)

	for m in modifier:
		modifier_out.append('%s ' % m)

	out += ''.join(var_out) + '\n' + ''.join(flag_out) + '\n' + ' '.join(modifier_out) + '}\n'

	return out

def newest_save():
	saves = glob.glob(os.path.expanduser(os.path.join('~', 'Documents', 'Paradox Interactive', 'Europa Universalis IV', 'save games', '*')))
	return max(saves, key=os.path.getmtime)

path = ""

default_map = parse_file(os.path.join(path, "map", "default.map"))

provnumber = int(default_map["max_provinces"])

climate = parse_file(os.path.join(path, "map", "climate.txt"))


with open(newest_save(), encoding='ISO-8859-1') as f:
	t = f.read()
	f.close()
	ttt = ['']
	textIndex = 0
	file_size_limit = 1024 * 48024  # Set desired file size limit (e.g., 1MB)
	current_file_size = 0
	
	for prov in glob.glob(os.path.join('history', 'provinces', '*.txt')):
		with open(prov, encoding='ISO-8859-1') as ff:
			tt = ff.read()
			ff.close()

			if '\n1.1.1' in tt:
				tt = tt[:tt.find('\n\n1.1.1')]

			idp = os.path.splitext(os.path.basename(prov))[0].split('-')[0].strip()
			if (idp not in default_map["only_used_for_random"] and not idp in default_map["lakes"] and not idp in default_map["sea_starts"] and not idp in climate['impassable']):
				print(idp)

				block = get_prov(idp, t)

				var = get_var(block)
				flag = get_flag(block)
				modifier = get_modifier(block)

				if len(var) == 0:
					var = 'clz=0.000'

				flag = flag.split('\n')
				var = var.split('\n')

				flag = [ff.split('=')[0] for ff in flag]
			
				history_entry = get_history(idp, var, flag, modifier)
				entry_size = len(history_entry.encode('ISO-8859-1'))

				if current_file_size + entry_size > file_size_limit:
					ttt.append('')
					textIndex += 1
					current_file_size = 0

				ttt[textIndex] += history_entry
				current_file_size += entry_size
			else:
				print("Skipping province %s" % idp)

	
	for country in glob.glob(os.path.join('history', 'countries', '*.txt')):
		with open(country, encoding='ISO-8859-1') as ff:
			tt = ff.read()
			ff.close()

			if '\n1.1.1' in tt:
				tt = tt[:tt.find('\n\n1.1.1')]
			
			tag = os.path.splitext(os.path.basename(country))[0].split('-')[0].strip()

			print(tag)

			block = get_country(tag, t)

			var = get_var(block)
			flag = get_flag(block)
			modifier = get_modifier2(block)

			if len(var) == 0:
				var = 'clz=0.000'

			flag = flag.split('\n')
			var = var.split('\n')
			
			flag = [ff.split('=')[0] for ff in flag]

			history_entry = get_history2(tag, var, flag, modifier)
			entry_size = len(history_entry)

			if current_file_size + entry_size > file_size_limit:
				ttt.append('')
				textIndex += 1
				current_file_size = 0

			ttt[textIndex] += history_entry
			current_file_size += entry_size


	event_structure = """
	country_event = {
		id = POP_Init.00%d
		title = no_localisation
		desc = no_localisation
		picture = MEIOU_AND_TAXES_eventPicture

		is_triggered_only = yes
		hidden = yes

		immediate = {
			hidden_effect = {
				%s
			}
		}
		option = {
			name = no_localisation
		}
	}
	"""
	for ind, tt in enumerate(ttt):
		ttt[ind] = event_structure % (ind + 1, tt)
		eventName = '00-POP_Init-%d.txt' % ind
		with open(os.path.join('events', eventName), 'w') as ff:
			ff.write(ttt[ind])
