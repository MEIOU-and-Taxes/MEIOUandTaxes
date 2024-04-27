start_text=''' Disp_Trade0_B: "'''
fill_text='''[Node%s]          NAME %s\n'''
end_text='''\n"'''

out = start_text
for x in range(1, 80, 1): #1 to 79 in steps of +1
    out += fill_text.replace("%s", str(x))
out += end_text

print(out)
input()