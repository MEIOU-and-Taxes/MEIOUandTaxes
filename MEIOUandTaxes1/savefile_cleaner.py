import re
import os
import glob
import traceback
import time
from math import ceil

SAVE_HEADER = "EU4txt".encode("iso-8859-1")  # First 6 chars of uncompressed savefile

try:
    class ProgressBar():
        def __init__(self, top, before='', after='', end='\n'):
            self.bef = before
            self.aft = after
            self.top = top
            self.end = end
            self.next = 0
        
        def show(self, progress):
            if not self.top:
                return False
            
            if not self.next:
                print(f"{self.bef} |{' '*22}| {self.aft}", end="")
                self.next = min(0.0001, ceil((progress + 1) / self.top * 21))
                return True
            
            if progress >= self.top:
                print(f"\r{self.bef} |{'█'*22}| {self.aft}", end=self.end)
                self.top = None
                return False
            
            if progress >= self.next:
                p = (progress+1) / self.top * 21
                self.next = ceil(p) * self.top / 21
                p = round(p)
                print(f"\r{self.bef} |█{'█'*p}{' '*(20-p)} | {self.aft}", end="")
                return True
            
            return True
    dir = __file__  # Find save games folder, searching upwards
    while dir != (dir := os.path.dirname(dir)):
        if os.path.isdir(os.path.join(dir, "save games")):
            os.chdir(os.path.join(dir, "save games"))
            break
        os.chdir(dir)
    else:
        raise ValueError("Could not find save games folder.")

    def is_uncompressed_file(file):  # Is an uncompressed eu4 savefile
        with open(file, "rb") as f:
            return f.read(6) == SAVE_HEADER
    
    def is_backup_file(file):
        return file[-11:] == "_backup.eu4"

    def is_clean_file(file):
        ...

    # List of possible savefiles
    files = [
        file for file in glob.iglob("**/*.eu4", recursive=True) if is_uncompressed_file(file) and not is_backup_file(file)
    ]

    print("Welcome to the eu4 save file cleaner! Select your unclean save file below: ")
    while True:  # Input file
        if len(files) <= 60:
            for i, file in enumerate(files):
                print(f"{i:>4}: {file}")
            inp = input("Type the number or name, or enter to use the latest save: ")
        else:
            inp = input("Type the savefile path, or enter to use the latest save: ")

        if not inp:  # Default option, use latest save
            files.sort(key=os.path.getmtime)
            file = files[0]
            break
        try:  # Get save by index
            inp = int(inp)
            file = files[inp]
            break
        except Exception:
            pass
        if inp in files:  # Get save name (in list)
            file = inp
            break
        try:  # Get save name (not in list)
            if not inp.endswith(".eu4"):
                inp += ".eu4"
            if is_uncompressed_file(inp):
                file = inp
                break
        except FileNotFoundError:
            print("Could not find specified file.")
        except ValueError:
            print("Unreadable file (is it compressed?)")

    backup = None
    while True:  # Output file
        inp = input("Type output filename, or enter for overwrite & backup: ")
        if not inp:  # Default option
            backup = file[:-4] + "_backup.eu4"
            if os.path.isfile(backup):
                if not input(f" '{backup}' exists, overwrite? (y/n): ").lower() in ("y", "yes"):
                    backup = None
                    continue
            out = file
            break
        elif not inp.endswith(".eu4"):
            inp += ".eu4"
        if os.path.isfile(inp):  # Overwrite protection
            if not input(f" '{inp}' exists, overwrite? (y/n): ").lower() in ("y", "yes"):
                continue
            out = inp
            break
        else:
            try:  # Try to create destination file
                with open(inp, "w") as f:
                    out = inp
                break
            except Exception:
                print("Could not access location or invalid filename.")

    with open(file, "r") as f:
        WS = str.maketrans('\n\t\r','   ')
        R_WS = re.compile(r"(?<=[={}]) +| +(?= )| +(?=[={} ])")
        R_NUM = re.compile(r" \b\S+=0\.000|(?<=[={}]) +| +(?= )| +(?=[={} ])")
        def format_text(text, reg):
            return re.sub(reg, '', text.translate(WS))
        text = []
        pos = 0
        print(f"Reading from '{file}'...", end = '')
        
        time1 = time.perf_counter()
        txt = f.read()
        for match in re.finditer(r'variables\=\{[^\}]*\}', txt):
            text.append(format_text(txt[pos:match.start()], R_WS))
            text.append(format_text(match.group(), R_NUM))
            pos = match.end()
        text.append(format_text(txt[pos:], R_WS))
        
        time2 = time.perf_counter()
        print(f"  Took {time2 - time1:.4f}s")
        del time1, time2
        
        sizes = (len(txt)/1024/1024, sum(map(len, text))/1024/1024)
        del txt

    if backup:
        print(f"Backing up '{file}' as '{backup}'")
        os.replace(file, backup)

    with open(out, "w") as o:
        print(f"Writing to '{out}'...", end="")
        o.write(''.join(text))
        print("  Done!\n")

        print(f"Reduced size by {sizes[0]-sizes[1]:.1f}MB, from {sizes[0]:.1f}MB to {sizes[1]:.1f}MB")
        input("Press enter to exit...")

except Exception:
    traceback.print_exc()
    input("Press enter to exit...")
