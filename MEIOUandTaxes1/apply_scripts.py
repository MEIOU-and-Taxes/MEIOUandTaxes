import os
import re
import glob
from queue import *
from threading import Thread
import time

py_block = re.compile('\#.*\".*?\".*')
py_string = re.compile('\".*?\"')
py_string2 = re.compile('#.*')
py_string3 = re.compile('(\[\[[\w&$]*\]|\^\^[\w&$]*\^|[\>\<\!\=]+|[\{\}\]^])')
def run(q, files):
	path1 = pathstart('decisions')
	while not q.empty():
		path = q.get()
		check = [True]
		while check[0]:
			check[0] = False
			if path1 in path:
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

def pathcont (text):
	return os.path.join('', text, '')

def pathstart (text):
	return os.path.join(text, '')

def pathend (text):
	return os.path.join('', text)


if __name__ == '__main__':
    try:
        output_path = os.path.expanduser(r'~\Documents\Paradox Interactive\Europa Universalis IV\mod\MEIOUandTaxes1')
        start = time.time()
        dont = ['Tools for Modding', 'graphicalculturetype.txt', pathcont('bookmarks'), pathcont('countries'), pathcont('country_colors'), pathcont('country_tags'),
                pathcont('cultures'), pathcont('event_modifiers'), pathcont('opinion_modifiers'), pathstart('map'), pathstart('interface'), pathstart('gfx'), pathcont('units'),
                pathcont('static_modifiers'), pathcont('countries'), pathcont('country_tags'), pathcont('province_names'), pathcont('tradenodes'), 'SYS-CensusDisplay.txt',
                pathcont('event_modifiers'), 'DISP-Trade_Bought.txt', 'DISP-Trade_Bought_2.txt', 'DISP-Trade_Bought_3.txt', 'DISP-Trade_Sold.txt', 'DISP-Trade_Sold_2.txt', 'DISP-Trade_Sold_3.txt']
        paths = [path for path in glob.glob(os.path.join('*', '**', '*.txt'), recursive=True) if not check_dont(path, dont)]

        files = dict()
        scripts = dict()

        for path in paths:
            print(path)
            files[path] = parse_file(path)

        dont = ['00-triggers.txt']
        print("Loading effects and triggers...")
        for path in glob.glob(os.path.join('common', 'scripted_effects', '*.txt')):
            paths.remove(path)
            for script in files[path]:
                scripts[script[0]] = script[2]

        for path in glob.glob(os.path.join('common', 'scripted_triggers', '*.txt')):
            paths.remove(path)
            for script in files[path]:
                if len(script[2]) > 1 and type(script[2]) == type(list()) and not check_dont(path, dont):
                    scripts[script[0]] = [['AND', '=', script[2]]]
                else:
                    scripts[script[0]] = script[2]

        print("Applying scripts to files...")
        q = Queue(maxsize=0)
        num_threads = min(20, len(paths))

        for i in range(len(paths)):
            q.put(paths[i])

        for i in range(num_threads):
            worker = Thread(target=run, args=(q, files))
            worker.start()

        q.join()

        print("Saving files...")
        for path in paths:
            save_path = os.path.join(output_path, os.path.relpath(path))
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w', encoding='ISO-8859-1') as f:
                f.write(reconstruct(files[path]))
        end = time.time()
        print((end - start))
    except Exception as e:
        print("An error occurred:", e)
        input("Press Enter to exit...")


