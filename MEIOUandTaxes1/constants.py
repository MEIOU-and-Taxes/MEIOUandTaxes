import os
import sys
import re
import glob

class MyRepl:
    def __init__(self, constants):
        self.constants = constants

    def repl(self, matchobj):
        out = matchobj.group(0)
        decorators = matchobj.group(1).split('~~')

        for item in decorators:
            item = item.split('~')

            out = re.sub(f'{item[1]}\s*=\s*\+?-?[0-9]*\.?[0-9]*', f'{item[1]} = {self.constants[item[0]]}', out)
        
        return out

def get_constants():
    out = dict()

    with open('constants.txt') as f:
        for line in f.readlines():
            ind = line.find('#')

            if ind >= 0:
                line = line[:ind]

            if line:
                key, val = [t.strip() for t in line.split(':')]

                out[key] = val
    
    return out

if __name__ == '__main__':
    paths = [path for path in glob.glob(os.path.join('*', '**', '*.txt'), recursive=True)]
    constants = get_constants()
    repl = MyRepl(constants)
    pattern = re.compile('{.+#.*`(.+)`')
    temp_marker = '`~`'

    noise = '--n' in sys.argv

    print("Updating")

    for path in paths:
        with open(path, 'r', encoding='ISO-8859-1') as f:
            t = f.read()

            if noise:
                print(path)

            if '`' in t and '~' in t:
                t = pattern.sub(repl.repl, t)

                with open(path, 'w', encoding='ISO-8859-1') as ff:
                    ff.write(t)

    print("Updating Complete")