import sys, os, winsound

def search(a):
    sys.stdout.write("Type 'y' if you only want exact copies\n")

    b = input()
    
    sys.stdout.write("Searching '%s'\n" % a)

    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if '.txt' in filename or '.yml' in filename or '.gui' in filename or '.gfx' in filename:
                with open(os.path.join(dirpath, filename), 'r', encoding='ISO-8859-1') as f:
                    t = f.read()

                    ind = t.find(a)

                    if b == 'y':
                        while ind + 1:
                            if (ind == 0 or t[ind - 1] in ' \n\t{}=') and (ind + len(a) >= len(t) or t[ind + len(a)] in ' \n\t{}='):
                                break
                            else:
                                t = t[:ind] + chr(ord(t[ind]) + 1) + t[ind + 1:]

                                ind = t.find(a)
                    
                    if ind + 1:
                        sys.stdout.write(os.path.join(dirpath, filename))

    sys.stdout.write('Search Complete\n')

    winsound.Beep(440, 500)
    winsound.Beep(440, 500)

    sys.stdout.write('Type something new if you want to search something else\n')
    sys.stdout.write("If not, type 'q' to quit\n")

sys.stdout.write("Type what you want to search\n")

a = input()

while True:
    search(a)

    a = input()

    if a == 'q':
        break
