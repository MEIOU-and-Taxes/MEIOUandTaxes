import math, sys

def make_binary_tree(tab, rank, start, end, trig, content):
    if end == start:
        return content.replace('%s', (no_supflu_0(str(end)))).replace('lsttb', tab)

    tstr = 'if = { limit = { %s }\nlsttb\t%s\nlsttb}\nlsttbelse = {\nlsttb\t%s\nlsttb}'

    if rank == 1:
        trig_new = trig.replace('%s', str(end))
            
        content_1 = content.replace('%s', str(end))
        content_2 = content.replace('%s', str(math.floor((end - start) / 2 + start)))
    else:
        trig_new = trig.replace('%s', (no_supflu_0(str(math.ceil((start + end) / 2)))))
        content_1 = make_binary_tree(tab + '\t', rank - 1, math.ceil((start + end) / 2), end, trig, content)
        content_2 = make_binary_tree(tab + '\t', rank - 1, start, math.ceil((start + end) / 2) - 1, trig, content)

    return (tstr % (trig_new, content_1, content_2)).replace('lsttb', tab)

def no_supflu_0(inp):
    return (inp + '.').rstrip('0').rstrip('.')

def calc_rank(prec, size):
    return math.log2(size / prec)

def logistic_reverse(output, midpnt, steepns, maxval, subtract):
    return round(math.log(maxval / (output + subtract) - 1) / -steepns + midpnt, 3)

sys.stdout.write('Precision\n')

prec = int(input())

sys.stdout.write('Start\n')

start = int(input())

sys.stdout.write('End\n')

end = int(input())

rank = math.ceil(calc_rank(prec, end - start + 1))

if rank == 0:
    sys.stdout.write('Precision greater than the total length')
else:
    sys.stdout.write('Trig\n')

    trig = input()

    sys.stdout.write('Content\n')

    content = input()

    with open('output.txt', 'w') as f:
        f.write(make_binary_tree('', rank, start, end, trig, content))
