import re
from queue import *
from threading import Thread
import time
py_block = re.compile('\#.*\".*?\".*')
py_string = re.compile('\".*?\"')
py_string2 = re.compile('#.*')
py_string3 = re.compile('(\[\[[\w&$]*\]|\^\^[\w&$]*\^|[\>\<\!\=]+|[\{\}\]^])')
def run(q, files, isWindows):
	while not q.empty():
		path = q.get()
		check = [True]
		while check[0]:
			if isWindows:
				check[0] = False
				if 'decisions\\' in path:
					files[path] = apply_script_to_decision(files[path], scripts, check)
				else:
					files[path] = apply_script(files[path], scripts, check)
			else:
				check[0] = False
				if 'decisions/' in path:
					files[path] = apply_script_to_decision(files[path], scripts, check)
				else:
					files[path] = apply_script(files[path], scripts, check)
		q.task_done()
	return True

def parse_block(block):
	block = py_block.sub('', block)
	strings = py_string.findall(block)
	block = py_string.sub(' %s ', block)
	block = py_string2.sub('\n', block)
	block = py_string3.sub(r' \1 ', block)
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

def apply_macro(file, macros, check=[False]):
	out = list()
	
	for f in file:
		if f and type(f) == type(list()):
			if f[0].count('^') == 2:
				check[0] = True
				
				name = f[0][1:-1]

				for foo in [expand_macro(f[1], f'&{name}&', item) for item in macros[name]]:
					out.extend(foo)
			else:
				out.append(apply_macro(f, macros, check))
		else:
			out.append(f)

	return out

def expand_macro(content, name, item):
	out = list()

	for c in content:
		if type(c) == type(list()):
			out.append(expand_macro(c, name, item))
		else:
			out.append(c.replace(name, item))

	return out
						
def apply_script(file, scripts, check=[False]):
	out = list()

	for f in file:
		if f[0] in scripts:
			check[0] = True
			
			if f[2] == 'yes':
				out.extend(apply_paras(scripts[f[0]], []))
			elif f[2] == 'no':
				out.append(['NOT', '=', apply_paras(scripts[f[0]], [])])
			else:
				out.extend(apply_paras(scripts[f[0]], f[2]))
		elif type(f[2]) != type(list()) or not f[2] or type(f[2][0]) != type(list()):
			out.append(f)
		else:
			out.append([f[0], f[1], apply_script(f[2], scripts, check)])
			
	return out

def apply_paras(script, paras):
	out = list()

	for section in script:
		if '[' in section[0]:
			for para in paras:
				if section[0][1:-1] == para[0]:
					out.extend(apply_paras(section[1], paras))

					break
		else:
			outout = list()
			
			for part in section[:2]:
				if '$' in part:
					foo = str(part)
					
					for para in paras:
						foo = foo.replace(f'${para[0]}$', para[2])

					outout.append(foo)
				else:
					outout.append(part)
					
			if type(section[2]) != type(list()):
				if '$' in section[2]:
					foo = str(section[2])
					
					for para in paras:
						foo = foo.replace(f'${para[0]}$', para[2])

					outout.append(foo)
				else:
					outout.append(section[2])
			else:
				outout.append(apply_paras(section[2], paras))

			out.append(outout)
				
	return out

def reconstruct(file, t=''):
	txt = ''

	for f in file:
		if f:
			if len(f) == 3 and type(f[0]) != type(list()) and type(f[1]) != type(list()):
				if type(f[2]) == type(list()):
					tail = ''
						
					if f[2]:
						if type(f[2][0]) != type(list()):
							tail = ' '.join(f[2])
						else:
							tail = '\n%s%s' % (reconstruct(f[2], t + '\t'), t)

					txt += '%s%s %s { %s}\n' % (t, f[0], f[1], tail)
				else:
					txt += '%s%s %s %s\n' % (t, f[0], f[1], f[2])
			elif len(f) == 2 and type(f[0]) != type(list()):
				txt += '%s[%s\n%s%s]\n' % (t, f[0], reconstruct(f[1], t + '\t'), t)

	return txt

def apply_script_to_decision(file, scripts, check):
	out = list()

	for decisions in file:
		foo = [decisions[0], decisions[1], []]
		
		for decision in decisions[2]:
			foo[2].append([decision[0], decision[1], apply_script(decision[2], scripts, check)])

		out.append(foo)

	return out

def check_dont(path, dont):
	for item in dont:
		if item in path:
			return True
		
	return False

def find_code(file, keywords):
	out = list()

	for f in file:
		if f[0] in keywords:
			out.extend([f[0],f[2]])
		elif type(f[2]) != type(list()) or not f[2] or type(f[2][0]) != type(list()):
			continue
		else:
			out.extend(find_code(f[2], keywords))
			
	return out

def remove_code(file, keywords):
	out = list()

	for f in file:
		if f[0] in keywords:
			continue
		else:
			out.append(f)
			
	return out

if __name__ == '__main__':
	import glob
	import os
	start = time.time()
	if os.name == 'nt':
		isWindows = 1
		# dont = ['Tools for Sub-Modding', 'graphicalculturetype.txt', '\\bookmarks\\', '\\countries\\', '\\country_colors\\', '\\country_tags\\', '\\cultures\\', '\\event_modifiers\\', '\\opinion_modifiers\\', 'map\\', 'interface\\', 'gfx\\', '\\units\\', '\\static_modifiers\\', '\\countries\\', '\\country_tags\\', '\\province_names\\', '\\tradenodes\\', 'SYS-CensusDisplay.txt', '\\event_modifiers\\']
		# paths = [path for path in glob.glob('*\\**\\*.txt', recursive=True) if not check_dont(path, dont)]
	else:
		isWindows = 0
	#	dont = ['Tools for Sub-Modding', 'graphicalculturetype.txt', '/bookmarks/', '/countries/', '/country_colors/', '/country_tags/', '/cultures/', '/event_modifiers/', '/opinion_modifiers/', 'map/', 'interface/', 'gfx/', '/units/', '/static_modifiers/', '/countries/', '/country_tags/', '/province_names/', '/tradenodes/', 'SYS-CensusDisplay.txt', '/event_modifiers/']
	# 	paths = [path for path in glob.glob('*/**/*.txt', recursive=True) if not check_dont(path, dont)]

	# files = dict()
	# scripts = dict()
	
	# for path in paths:
	# 	print(path)
	# 	files[path] = parse_file(path)

	# dont = ['00-triggers.txt']
	# print("Loading effects and triggers...")
	# if isWindows:
	# 	for path in glob.glob('common\\scripted_effects\\*.txt'):
	# 		paths.remove(path)
	# 		for script in files[path]:
	# 			scripts[script[0]] = script[2]

	# 	for path in glob.glob('common\\scripted_triggers\\*.txt'):
	# 		paths.remove(path)
	# 		for script in files[path]:
	# 			if len(script[2]) > 1 and type(script[2]) == type(list()) and not check_dont(path, dont):
	# 				scripts[script[0]] = [['AND', '=', script[2]]]
	# 			else:
	# 				scripts[script[0]] = script[2]
	
	# else:
	# 	for path in glob.glob('common/scripted_effects/*.txt'):
	# 		paths.remove(path)
	# 		for script in files[path]:
	# 			scripts[script[0]] = script[2]

	# 	for path in glob.glob('common/scripted_triggers/*.txt'):
	# 		paths.remove(path)
	# 		for script in files[path]:
	# 			if len(script[2]) > 1 and type(script[2]) == type(list()) and not check_dont(path, dont):
	# 				scripts[script[0]] = [['AND', '=', script[2]]]
	# 			else:
	# 				scripts[script[0]] = script[2]
	
	
	
	# print("Applying scripts to files...")
	# q = Queue(maxsize=0)
	# num_threads = min(20, len(paths))

	# for i in range(len(paths)):
	# 	q.put(paths[i])

	# for i in range (num_threads):
	# 	worker = Thread(target=run,args=(q,files,isWindows))
	# 	worker.start()

	# q.join()

	paths = [parse_file("events\\FE-BRB.txt"), parse_file("events\\FE-BRB.txt")]

	modfiles = dict()
	modifiers = []
	keywords = ["add_country_modifier", "add_province_modifier", "add_ruler_modifier", "add_permanent_province_modifier", "add_disaster_modifier", "extend_province_modifier", "add_province_triggered_modifier"]

	print("Loading modifier files...")
	
	if isWindows:
		modpaths = [path for path in glob.glob('common\\event_modifiers\\*.txt' or 'common\\province_triggered_modifiers\\*.txt')]
	else:
		modpaths = [path for path in glob.glob('common/event_modifiers/*.txt' or 'common/province_triggered_modifiers/*.txt')]

	for path in modpaths:
		print(path)
		modfiles[path] = parse_file(path)
		for modifier in modfiles[path]:
			modifiers.append(modifier[0])

	modifierlist = [find_code(path, keywords) for path in paths]
	used_modifiers = []
	for x in modifierlist:
		for y in x[1::2]:
			for z in y:
				if z[0] == "name":
					if z[2] not in used_modifiers:
						used_modifiers.append(z[2])
					break

	print("Finding surplus modifiers...")
	missing_modifiers = [modifier for modifier in modifiers if modifier not in used_modifiers]
	for missing in missing_modifiers:
		print(missing)

	print("Writing modifier files...")
	for path in modpaths:
		text = modfiles[path]
		text = remove_code(text, missing_modifiers)
		with open(path, 'w', encoding='ISO-8859-1') as f:
			f.write(reconstruct(text))
	end = time.time()
	print((end - start))


