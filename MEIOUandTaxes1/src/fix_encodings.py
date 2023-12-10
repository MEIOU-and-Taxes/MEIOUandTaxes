from glob import iglob
def reencode(enc, ending):
	files = iglob('**/*' + ending, recursive=True)
	for fn in files:
		content = None
		with open(fn,"rb") as f:
			ff = f.read()
			content = ff.decode(enc)
		with open(fn, 'w', encoding = enc, newline='') as f:
			if content:
				f.write(content)
if __name__ == '__main__':
	reencode('iso-8859-1', '.txt')
	reencode('utf-8-sig', '.yml')