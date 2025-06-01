import os, sys, re, glob, shutil, time, multiprocessing, runpy

__all__ = [ 'compile' ]

py_block = re.compile('\\#.*\".*?\".*')
py_string = re.compile('\".*?\"')
py_string2 = re.compile('#.*')
py_string3 = re.compile('(\\[\\[[\\w&$]*\\]|\\^\\^[\\w&$]*\\^|[\\>\\<\\!\\=]+|[\\{\\}\\]^])')

script_build_path = 'build_workspace'

def parse_block(block):
	block = py_block.sub('', block)
	strings = py_string.findall(block)
	block = py_string.sub(' %s ', block)
	block = py_string2.sub('\n', block)
	block = py_string3.sub(r' \1 ', block)
	block = block.strip()

	if block:
		block = re.split('\\s+', block)

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

	if len(script) and all(type(part) == str and part != '=' for part in script):
		script = ' '.join(script)
		for para in paras:
			script = script.replace(f'${para[0]}$', para[2])
		return [script]

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

def reconstruct_compressed(file):
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
							tail = '%s' % (reconstruct_compressed(f[2]))

					txt += '%s%s{%s}' % (f[0], f[1], tail)
				else:
					txt += '%s%s%s ' % (f[0], f[1], f[2])
			elif len(f) == 2 and type(f[0]) != type(list()):
				txt += '[%s%s]' % (f[0], reconstruct_compressed(f[1]))

	return txt

def apply_script_to_decision(file, scripts, check):
	out = list()

	for decisions in file:
		foo = [decisions[0], decisions[1], []]
		
		for decision in decisions[2]:
			foo[2].append([decision[0], decision[1], apply_script(decision[2], scripts, check)])

		out.append(foo)

	return out

scripts = dict()
def load_scripts():
	for path in glob.iglob(os.path.join('src', 'common', 'scripted_effects', '*.txt')):
		parsed = parse_file(path)
		for script in parsed:
			scripts[script[0]] = script[2]
	for path in glob.iglob(os.path.join('src', 'common', 'scripted_triggers', '*.txt')):
		parsed = parse_file(path)
		for script in parsed:
			if len(script[2]) > 1 and type(script[2]) == type(list()) and not path.endswith( '00-triggers.txt' ):
				scripts[script[0]] = [['AND', '=', script[2]]]
			else:
				scripts[script[0]] = script[2]
	#highly cursed, johan smite me
	for path in glob.iglob(os.path.join('src', 'customizable_localization', '*.script')):
		parsed = parse_file(path)
		for script in parsed:
			scripts[script[0]] = script[2]

decisionpath = os.path.join( 'src', 'decisions' )
def compile_file(path, compress):
	if not scripts:
		load_scripts()
	file = parse_file(path)
	check = [True]
	while check[0]:
		check[0] = False
		if path.startswith(decisionpath):
			file = apply_script_to_decision(file, scripts, check)
		else:
			file = apply_script(file, scripts, check)
	if path.startswith( script_build_path + os.sep ):
		relpath = os.path.relpath( path, script_build_path )
	else:
		relpath = os.path.relpath( path, 'src' )
	buildpath = os.path.join( 'build', relpath )
	os.makedirs( os.path.dirname( buildpath ), exist_ok=True )
	with open(buildpath, 'w', encoding='ISO-8859-1') as f:
		if compress:
			f.write(reconstruct_compressed(file))
		else:
			f.write(reconstruct(file))

# helper functions since we can only pass one argument to multiprocess pool
def compile_and_save_uncompressed(path):
	compile_file(path, False)
def compile_and_save_compressed(path):
	compile_file(path, True)

def link_file ( filepath, destpath ):
	os.makedirs( os.path.dirname( destpath ), exist_ok=True )
	os.link( filepath, destpath )

def compile(compress=False, parse_init=True, debug=False):
	start = time.time()

	# files/paths to run through parsing
	parse = [
		'common',
		'customizable_localization',
		'decisions',
		'dlc_metadata',
		'events',
		'hints',
		'history',
		'localisation',
		'missions',
		'music'
	]

	# files/paths to link instead of parsing
	link = [
		[ 'common', 'graphicalculturetype.txt' ],
		[ 'common', 'ages' ],
		[ 'common', 'bookmarks' ],
		[ 'common', 'countries' ],
		[ 'common', 'country_colors' ],
		[ 'common', 'country_tags' ],
		[ 'common', 'cultures' ],
		[ 'common', 'event_modifiers' ],
		[ 'common', 'opinion_modifiers' ],
		[ 'common', 'province_names' ],
		[ 'common', 'scripted_triggers' ],
		[ 'common', 'scripted_effects' ],
		[ 'common', 'static_modifiers' ],
		[ 'common', 'tradenodes' ],
		[ 'common', 'units' ],
		[ 'customizable_localization', 'DISP-Trade_Bought.txt' ],
		[ 'customizable_localization', 'DISP-Trade_Bought_2.txt' ],
		[ 'customizable_localization', 'DISP-Trade_Bought_3.txt' ],
		[ 'customizable_localization', 'DISP-Trade_Sold.txt' ],
		[ 'customizable_localization', 'DISP-Trade_Sold_2.txt' ],
		[ 'customizable_localization', 'DISP-Trade_Sold_3.txt' ],
		[ 'events', 'SYS-CensusDisplay.txt' ],
		'gfx',
		[ 'history', 'countries' ],
		'interface',
		'map',
		'descriptor.mod',
		'thumbnail.png',
		'meiou.txt',
		'checksum_manifest.txt',
		'savefile_cleaner.py'
	]

	if not parse_init:
		link.extend([
			[ 'events', '00-POP_Init-0.txt' ],
			[ 'events', '00-POP_Init-1.txt' ],
			[ 'events', '00-POP_Init-2.txt' ]
		])

	parse = [ os.path.join( *p ) if type( p ) is list else p for p in parse ]
	link = [ os.path.join( *p ) if type( p ) is list else p for p in link ]

	def check_path_link ( path ):
		for p in link:
			if path.startswith( p ):
				return True
		return False

	def check_path_parse ( path ):
		for p in parse:
			if path.startswith( p ):
				return not check_path_link( path )
		return False

	print( 'Clearing build directory...' )
	if ( os.path.exists( 'build' ) ):
		shutil.rmtree( 'build' )
	if os.path.exists( script_build_path ):
		shutil.rmtree( script_build_path )

	print( 'Running build scripts...' )
	for script in glob.glob( os.path.join( 'src', 'build_scripts', '*.py' ) ):
		runpy.run_path( script, { "outdir": script_build_path }, '__build__' )

	print( 'Reading file tree...' )

	parsepaths = []
	linkpaths = []

	files = glob.glob( os.path.join( 'src', '**' ), recursive=True )
	if not script_build_path.startswith( 'src' ):
		files += glob.glob( os.path.join( script_build_path, '**' ), recursive=True )
	for path in files:
		if os.path.isfile( path ):
			if path.startswith( os.path.join( script_build_path + os.sep ) ):
				relpath = os.path.relpath( path, script_build_path )
			else:
				relpath = os.path.relpath( path, 'src' )
			if check_path_parse( relpath ):
				if relpath.endswith( '.txt' ):
					parsepaths.append( path )
				else:
					linkpaths.append( path )
			elif check_path_link( relpath ):
				linkpaths.append( path )

	if 'fork' in multiprocessing.get_all_start_methods():
		multiprocessing.set_start_method('fork')
		print( 'Loading scripts...' )
		load_scripts()

	file_count = len(parsepaths)
	print(f"Compiling {file_count} files...")
	if debug:
		print(f"DEBUG: Compiling sequentially (slower)")
	print(f'0% done', end='')
	if not debug:
		with multiprocessing.Pool() as pool:
			if compress:
				compiled_files_it = pool.imap_unordered(compile_and_save_compressed, parsepaths, max(1, round(file_count/1000)))
			else:
				compiled_files_it = pool.imap_unordered(compile_and_save_uncompressed, parsepaths, max(1, round(file_count/1000)))
			for i in range(file_count):
				next(compiled_files_it)
				progress = 100*(i+1)/file_count
				sys.stdout.write('\x1b[2k') # clear line
				print(f'\r{progress:.1f}% done', end='')
	else:
		for i, f in enumerate(parsepaths):
			if compress:
				compile_and_save_compressed(f)
			else:
				compile_and_save_uncompressed(f)
			progress = 100*(i+1)/file_count
			sys.stdout.write('\x1b[2k') # clear line
			print(f'\r{progress:.1f}% done', end='')

	print("\nLinking static files...")
	for path in linkpaths:
		if path.startswith( script_build_path ):
			destpath = os.path.relpath( path, script_build_path )
		else:
			destpath = os.path.relpath( path, 'src' )
		destpath = os.path.join( 'build', destpath )
		link_file( path, destpath )

	end = time.time()
	print((end - start))

if __name__ == '__main__':
	compile()
