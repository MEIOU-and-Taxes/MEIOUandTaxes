###########################
#  M&T Utility Run Files  #
###########################

### What is a run file?

	A "run file" is a file that contains a code effect for eu4.
	It can be executed using a console command. 
	The effect will be executed immediately, under the root scope of the country doing the command.

### How to use run files?

	In the game, do "run [effectfilename]" in the console.
	For example, to run "mt_count_provinces", do "run mt_count_provinces.txt".

	Some run files will alter the game in progress, others will output data.

	This data can be found in Documents/Paradox Interactive/Europa Universalis IV/logs/game.log
	As that file keeps track of many things happening in the game, it's best to pause the game to execute 
	run files and check their results. Otherwise, the result may get buried under other game events.

	If the console says "Executed [effectfilename].txt", the file has been run successfully.

	If the console says "Cannot find file [effectfilename].txt or does not say anything,
	check that you have written the run file name correctly.

	Some run files require the selection of one or several provinces. In this case, pause the game 
	and start the construction of "Select Province" buildings in those provinces.
	Advance the game by one single day before running the file.
	If the file requires just one province but you build "Select Province" in several, one of these
	provinces will be chosen at random.

### Run files list

	mt_count_provinces.txt

Counts the amount of provinces in each continent and the world, then compares the sum.

	mt_indexes.txt

Exports names and indexes of cultures and religions