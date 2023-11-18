MT_grapher is a python script to graph various data about M&T, specifically data regarding economic simulations.

	1. Install python
	
	2. Install the plotting library with 'python -m pip install matplotlib' console command
	
	3. Move MT_grapher.py, all_graphs.py and graph_pages.csv to the folder Your Documents/Paradox Interactive/Europa Universalis IV/logs
	
	4. Start a game of M&T 3.0 as Mapuche (South African native), you can change tag with the console to continue a regular game with logging
	
	5. When you want to see the logs, double-click on MT_grapher.py
	
Eu4 will delete game.log every time you close the game. The grapher gives you a handy backup tool to preserve past game.logs, simply click on 'Backup game.log' after closing the game. The grapher will include these log backups when you view graphs. At the end of your campaign, don't forget to delete all the backed-up game.logs in the log folder! Right now there is only one continuous backup, multiple campaigns are not yet supported.

To add a new graph:

	1. Ensure data is logged in M&T code
	
	2. Add a function to plot the data in all_graphs.py, similar to the others there
	
		- The function name needs to start with 'graph'
		- The rest of the function name will be the button name (_ replaced with spaces), keep it short and unique
		- The function should have a docstring (unassigned string at the top), this is a more detailed description
	
	3. Add the button name to graph_pages.csv, at the position you want it to be
	
		- New pages are added by starting a line with ':'
		- The number of columns and rows in each page can vary
		- Python will complain if there are duplicate/missing entries