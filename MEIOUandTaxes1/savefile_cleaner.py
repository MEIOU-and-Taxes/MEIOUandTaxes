
import re
import os
import glob
import time
from math import ceil
from traceback import print_exc

try:
    SAVE_HEADER = "EU4txt\n".encode("iso-8859-1")
    print(SAVE_HEADER)
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

        def add(self, item):
            self.show(len(item))
            return item

        def done(self):
            self.show(self.top)

    dir = __file__  # Find save games folder, searching upwards
    while dir != os.path.dirname(dir):
        dir = os.path.dirname(dir)
        if os.path.isdir(os.path.join(dir, "save games")):
            os.chdir(os.path.join(dir, "save games"))
            break
        os.chdir(dir)
    else:
        raise ValueError("Could not find save games folder.")

    def is_valid_file(file):  # Is an uncompressed eu4 savefile
        with open(file, "rb") as f:
            t = f.read(7)
            if not t[:6] == SAVE_HEADER[:6]:
                return 0  # compressed file
            if not t[6] == SAVE_HEADER[6]:
                return -1  # already cleaned file
            return 1  # valid file
    
    def is_backup_file(file):
        return file[-11:] == "_backup.eu4"

    # List of possible savefiles
    files = [
        file for file in glob.iglob("**/*.eu4", recursive=True) if not is_backup_file(file) and is_valid_file(file) == 1
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
            v = int(inp)
            if 0 <= v < len(files):
                file = files[v]
                break
        except Exception:
            pass
        if inp in files:  # Get save name (in list)
            file = inp
            break
        try:  # Get save name (not in list)
            if not inp.endswith(".eu4"):
                inp += ".eu4"
            v = is_valid_file(inp)
            if v == -1:
                if not input('File is already cleaned, continue anyways? (y/n): ').lower() in ('y', 'yes'):
                    continue
                file = inp
                break
            elif v == 1:
                file = inp
                break
            else:
                print("File is compressed and cannot be read.")
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
        time1 = time.perf_counter()
        txt = f.read()
        pb = ProgressBar(len(txt), f"Reading from '{file}'... ", end='')
        for match in re.finditer(r'variables\=\{[^\}]*\}', txt):
            text.append(format_text(pb.add(txt[pos:match.start()]), R_WS))
            text.append(format_text(pb.add(match.group()), R_NUM))
            pos = match.end()
        text.append(format_text(pb.add(txt[pos:]), R_WS))
        pb.done()
        
        time2 = time.perf_counter()
        print(f"  Took {time2 - time1:.4f}s")
        
        sizes = (len(txt)/1024/1024, sum(map(len, text))/1024/1024)

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
    print_exc()
    input("Press enter to exit...")
