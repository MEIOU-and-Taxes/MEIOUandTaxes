#################################################
#												#
#	Courtesy of Dr. Njitram from the KR team	#
#												#
#################################################


from codecs import open
import sys
from os import listdir
import os


def event(cpath):
	# immediate = {log = "[Root.GetName]: event "+ id + "\n"}  # autolog
	for filename in listdir(cpath + "\\events"):
		if ".txt" in filename:
			outputfile = open(cpath + "\\events\\" + filename, 'r', 'iso-8859-1')
			size = os.path.getsize(cpath + "\\events\\" + filename)
			if size < 100:
				continue
			lines = outputfile.readlines()
			outputfile.close()
			outputfile = open(cpath + "\\events\\" + filename, 'w', 'iso-8859-1')
			outputfile.truncate()
			for line in lines:
				if 'immediate = {log = ' not in line:
					outputfile.write(line)
				else:
					outputfile.write("")


def decision(cpath):
	# immediate = {log = "[Root.GetName]: decision "+ id + "\n"}  # autolog
	for filename in listdir(cpath + "\\decisions"):
		if ".txt" in filename and filename.startswith('_') is False and 'categories' not in filename:
			outputfile = open(cpath + "\\decisions\\" + filename, 'r', 'iso-8859-1')
			size = os.path.getsize(cpath + "\\decisions\\" + filename)
			if size < 100:
				continue
			lines = outputfile.readlines()
			outputfile.close()
			outputfile = open(cpath + "\\decisions\\" + filename, 'w', 'iso-8859-1')
			outputfile.truncate()
			for line in lines:
				if 'log = "[GetDateText]' not in line:
					outputfile.write(line)
				else:
					outputfile.write("")


def mission(cpath):
	# immediate = {log = "[Root.GetName]: mission "+ id + "\n"}  # autolog
	for filename in listdir(cpath + "\\missions"):
		if ".txt" in filename and filename.startswith('_') is False and 'categories' not in filename:
			outputfile = open(cpath + "\\missions\\" + filename, 'r', 'iso-8859-1')
			size = os.path.getsize(cpath + "\\missions\\" + filename)
			if size < 100:
				continue
			lines = outputfile.readlines()
			outputfile.close()
			outputfile = open(cpath + "\\missions\\" + filename, 'w', 'iso-8859-1')
			outputfile.truncate()
			for line in lines:
				if 'log = "[GetDateText]' not in line:
					outputfile.write(line)
				else:
					outputfile.write("")


def main():
	cpath = os.path.dirname(os.path.abspath(__file__))
	ok = 0
	print("#########################################################\r\n#							#\r\n#	Courtesy of Dr. Njitram from the KR team	#\r\n#							#\r\n#########################################################")
	event(cpath)
	decision(cpath)
	mission(cpath)
if __name__ == "__main__":
	main()

