#################################################
#												#
#	Courtesy of Dr. Njitram from the KR team	#
#												#
#################################################


from codecs import open
import sys
from os import listdir
import time
import os
import re


def check_triggered(line_number, lines):
	if line_number == len(lines) or line_number == len(lines)-1 or line_number == len(lines)-2 :
		return True
	if '}' in lines[line_number+2] or 'days' in lines[line_number+2]:
		#print("1: Found Triggered Event at line: " + line_number.__str__())
		return True
	if '}' in lines[line_number+1] or 'days' in lines[line_number+1]:
		#print("1: Found Triggered Event at line: " + line_number.__str__())
		return True
	if '}' in lines[line_number] or 'days' in lines[line_number]:
		#print("1: Found Triggered Event at line: " + line_number.__str__())
		return True
	for i in range(line_number, len(lines)):
		string = lines[i].strip()
		if string.startswith('#') is True:
			continue
		if string.startswith('}') is True or 'days' in string:
			#print("2: Found Triggered Event at line: " + i.__str__())
			return True
		elif string != "":
			#print("3: Found normal Event at line: " + i.__str__())
			return False
	return False

def event(cpath):
	ttime = 0
	# immediate = {log = "[Root.GetName]: event "+ id + "\r\n"}  # autolog
	for filename in listdir(cpath + "\\events"):
		if ".txt" in filename:
			file = open(cpath + "\\events\\" + filename, 'r', 'iso-8859-1')
			lines = file.readlines()
			size = os.path.getsize(cpath + "\\events\\" + filename)
			if size < 100:
				continue
			event_id = None
			line_number = 0
			triggered = False
			ids = []
			idss = []

			timestart = time.time()
			for line in lines:
				line_number += 1
				if line.strip().startswith('#') or 'immediate = {log = ' in line:
					continue
				if '#' in line:
					line = line.split('#')[0]
				if 'country_event' in line: #New Event
					if check_triggered(line_number, lines) is False:
						if "}" not in line or "days" not in line:
							new_event = True
							if event_id is not None:
								triggered = False
						else:
							triggered = True
							new_event = False
							#print("1: Found Triggered Event at line: " + line_number.__str__())
					else:
						triggered = True
						new_event = False
				if line.strip().startswith('id') and new_event is True and 'immediate = {log =' not in lines[line_number+1]:
					if triggered is False:
						new_event = False
						event_id = line.split('=')[1].strip()
						idss.append(event_id)
						ids.append(line_number)
					else:
						triggered = False
			time1 = time.time() - timestart
			line_number = 0
			outputfile = open(cpath + "\\events\\" + filename, 'w', 'iso-8859-1')
			outputfile.truncate()
			for line in lines:
				line_number += 1
				backup = ''
				if line_number in ids:
					event_id = idss[ids.index(line_number)]
					if '#' in event_id:
						event_id = event_id.split('#')[0].strip()
					if '.' not in event_id:
						outputfile.write(line)
						continue
					if '#' in line and line.strip().startswith('#') is False:
						backup = '#' + line.split('#')[1].strip()
					if backup is '':
						replacement_text = "\tid = " + event_id + "\r\n\timmediate = {log = \"[GetDateText]: [Root.GetName]: event " + event_id + "\"}\r\n"
					else:
						replacement_text = "\tid = " + event_id + ' ' + backup + "\r\n\timmediate = { log = \"[GetDateText]: [Root.GetName]: event " + event_id + "\"}\r\n"
					outputfile.write(replacement_text)
					#print("Inserted loc at {0} in file {1}".format(line_number.__str__(), filename))
				else:
					outputfile.write(line)
			time2 = time.time() - timestart - time1

			#print(filename + " 1: %.3f ms  2: %.3f ms" % (time1*1000, time2*1000))
			ttime += time1 + time2
	return ttime

def decision(cpath):
	ttime = 0
	# log = "[GetDateText] [Root.GetName]: decision (remove) name"
	#common\decisions
	#for filename in listdir(cpath + "\\common\\decisions"):
	for filename in listdir(cpath + "\\decisions"):
		if ".txt" in filename:
			file = open(cpath + "\\decisions\\" + filename, 'r', 'iso-8859-1')
			size = os.path.getsize(cpath + "\\decisions\\" + filename)
			if size < 100:
				continue
			lines = file.readlines()
			line_number = 0
			level = 0
			ids = [] #array of the names
			idss = [] #line numbers of effect
			timestart = time.time()
			for line in lines:
				line_number += 1
				if '#' in line:
					if line.strip().startswith("#") is True:
						continue
					else:
						line = line.split('#')[0]
				if '= {' in line or '={' in line:
					if level == 1:
						ids.append(line.split('=')[0].strip())
				if 'effect' in line and '_effect' not in line:
					if 'log = \"[GetDateText]:' not in lines[line_number]:
						idss.append(line_number)
				if '{' in line:
					level += line.count('{')
				if '}' in line:
					level -= line.count('}')

			time1 = time.time() - timestart
			line_number = 0

			outputfile = open(cpath + "\\decisions\\" + filename, 'w', 'iso-8859-1')
			outputfile.truncate()
			for line in lines:
				line_number += 1
				if line_number in idss:
					dec_id = ids[idss.index(line_number)]
					if dec_id in ["{", "}"]:
						dec_id = "Error, focus name not found"
					if '}' in line:
						temp = line.split("{")
						replacement_text = temp[0] + "{\r\n\r\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Decision " + dec_id + "\"\r\n" + "{".join(temp)[len(temp[0])+1:] + "\r\n"
					else:
						replacement_text = "\t\teffect = {\r\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Decision " + dec_id + "\"\r\n"
					outputfile.write(replacement_text)
				else:
					outputfile.write(line)
			time2 = time.time() - timestart - time1

			#print(filename + " 1: %.3f ms  2: %.3f ms" % (time1*1000, time2*1000))
			ttime += time1 + time2
	return ttime


def mission(cpath):
	ttime = 0
	# log = "[GetDateText] [Root.GetName]: missions (remove) name"
	#missions
	#for filename in listdir(cpath + "\\missions"):
	for filename in listdir(cpath + "\\missions"):
		if ".txt" in filename:
			file = open(cpath + "\\missions\\" + filename, 'r', 'iso-8859-1')
			size = os.path.getsize(cpath + "\\missions\\" + filename)
			if size < 100:
				continue
			lines = file.readlines()
			line_number = 0
			level = 0
			ids = [] #array of the names
			idss = [] #line numbers of effect
			timestart = time.time()
			for line in lines:
				line_number += 1
				if '#' in line:
					if line.strip().startswith("#") is True:
						continue
					else:
						line = line.split('#')[0]
				if '= {' in line or '={' in line:
					if level == 1 and not 'potential' in line:
						ids.append(line.split('=')[0].strip())
				if 'effect' in line and '_effect' not in line:
					if 'log = \"[GetDateText]:' not in lines[line_number]:
						idss.append(line_number)
				if '{' in line:
					level += line.count('{')
				if '}' in line:
					level -= line.count('}')

			time1 = time.time() - timestart
			line_number = 0

			outputfile = open(cpath + "\\missions\\" + filename, 'w', 'iso-8859-1')
			outputfile.truncate()
			for line in lines:
				line_number += 1
				if line_number in idss:
					dec_id = ids[idss.index(line_number)]
					if '}' in line:
						temp = line.split("{")
						replacement_text = temp[0] + "{\r\n\r\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Mission " + dec_id + "\"\r\n" + "{".join(temp)[len(temp[0])+1:] + "\r\n"
					else:
						replacement_text = "\t\teffect = {\r\n\t\t\tlog = \"[GetDateText]: [Root.GetName]: Mission " + dec_id + "\"\r\n"
					outputfile.write(replacement_text)
				else:
					outputfile.write(line)
			time2 = time.time() - timestart - time1

			#print(filename + " 1: %.3f ms  2: %.3f ms" % (time1*1000, time2*1000))
			ttime += time1 + time2
	return ttime


def main():
	cpath = sys.argv[1]
	ok = 0
	print("#########################################################\r\n#							#\r\n#	Courtesy of Dr. Njitram from the KR team	#\r\n#							#\r\n#########################################################")
	for string in sys.argv:
		if ok < 2:
			ok += 1
		else:
			cpath += ' ' + string
	ttime = 0
	ttime += event(cpath)
	ttime += decision(cpath)
	ttime += mission(cpath)
	print("Total Time: %.3f ms" % (ttime * 1000))

if __name__ == "__main__":
	main()