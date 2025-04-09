###########
# General #
###########

- M&T Paradox Script highlighting

	This file colors in keywords for Paradox code, and includes Meiou & Taxes things.
	In Notepad++, go to Menu, Language, Define your language. Import "MT_highlight.xml" as a new language and save it under a name of your choice.
	The file will be updated occasionally, adding new things. Be sure to import it again occasionally.

	Localisation files should use the built-in YAML language highlighting instead.

- Color scheme

	The highlighting file has text colors suited for the Monokai theme (dark mode). You can enable this theme in Menu, Settings, Style Configurator. Also turn on "Enable global background color".
	If you prefer a different theme, feel free to change the highlighting colors in "Define your language".

############
# Settings #
############

- Tab highlighting

	Tabs are important to keep the code organised. Notepad can show non-intrusive lines where tabs are, to make them easy to count and keep track of.
	In the Notepad++ top bar, turn on "Show Indent Guide".

- Line wrap

	Since localisations cannot have actual line breaks in a single text, long descriptions and modifier text can lead to extremely wide files.
	These require lots of scrolling and are uncomfortable to work with.  
	In settings, set "Line Wrap" to "indent". In the Notepad++ top bar, turn on "Line Wrap".

- Comment folding

	The highlight file enables comment folding. Click on the "[-]" box to the right of comment blocks to hide the comments and make the entire file more compact and readable.

##########
# Macros #
##########

Put shortcuts.xml into %appdata%/Notepad++ to skip recording the macros (merge the files manually if you already have macros recorded)

- Commenting (alt + Q, alt + W)

	Use the following macros to quickly comment/uncomment code. Simply select the relevant lines of code and do the macro key combination.
	To comment code, replace "^" with "^#" on selected text in "regular expression" replacement mode.
	To uncomment code, replace "^#" with "^".

- \n replacement (alt + E, alt + R)

	Use the following macros to convert localisation line breaks into actual line breaks and back, very useful for editing large structured modifier localisations.
	To convert \n to newline, replace "\\n" with "\n" on selected text in "extended" replacement mode.
	To convert newline back to \n, replace "\n" with "\\n".

- log data cleanup (alt + T)

	Use this macro to quickly remove everything from game.log except for run file outputs. You can refresh the file using control + R (without saving) to get back the original file state.
	Replace "^((?!\[eff).*?\n)|^(\[effectimplementation\.cpp:.+?\]: EVENT \[.+?\]:)(.*?$)" with "$3" in "regular expression" replacement mode.