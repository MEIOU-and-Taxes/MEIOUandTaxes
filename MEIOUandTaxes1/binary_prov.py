import math, sys
import os

def parse_line(line):
    s = line.strip()
    ss = s.split('"')
    tokens = []
    for i,sss in enumerate(ss):
        if i%2==0:
            sss = sss.replace("="," = ").replace("{"," { ").replace("}"," } ")
            if "#" in sss:
                sss = sss.split("#")[0]
                tokens.extend(sss.split())
                return tokens
            tokens.extend(sss.split())
        else:
            tokens.append('"%s"' % sss)
    return tokens

def parse_file(fn):
    def update(dic, new):
        if isinstance(new, dict):
            new = new.items()
        for key, val in new:
            if key not in dic:
                dic[key] = val
            elif isinstance(dic[key], list):
                dic[key].append(val)
            else:
                dic[key] = [dic[key], val]
    d = {}
    names = []
    stack = [(d,"")]
    tokens = []
    key = ""
    with open(fn,"rb") as f:
        ff = f.read()
        fff = ff.decode("iso-8859-1")
        for line in fff.splitlines():
            tokens += parse_line(line)
        for token in tokens:
            if token == "=":
                key = names.pop()
            elif token == "{":
                dd = {}
                update(stack[-1][0], {key: dd})
                stack.append((dd,key))
                key = ""
            elif token == "}":
                if len(stack[-1][0]):
                    update(stack.pop()[0], [(n,n) for n in names])
                else:
                    k = stack.pop()[1]
                    stack[-1][0][k] = []
                    update(stack[-1][0], [(k,n) for n in names])
                names = []
            else:
                names.append(token)
                if key:
                    update(stack[-1][0], {key: names.pop()})
                    key = ""
    return d


def make_binary_tree(tab, rank, start, end, trig, content):
    if end == start:
        return content.replace('%s', (no_supflu_0(str(provinces[end-1])))).replace('lsttb', tab)

    tstr = 'if = { limit = { %s }\nlsttb\t%s\nlsttb}\nlsttbelse = {\nlsttb\t%s\nlsttb}'

    if rank == 1:
        trig_new = trig.replace('%s', str(provinces[end-1]))
            
        content_1 = content.replace('%s', str(provinces[end-1]))
        content_2 = content.replace('%s', str(provinces[math.floor((end - start) / 2 + start)-1]))
    else:
        trig_new = trig.replace('%s', (no_supflu_0(str(provinces[math.ceil((start + end) / 2)-1]))))
        content_1 = make_binary_tree(tab + '\t', rank - 1, math.ceil((start + end) / 2), end, trig, content)
        content_2 = make_binary_tree(tab + '\t', rank - 1, start, math.ceil((start + end) / 2) - 1, trig, content)

    return (tstr % (trig_new, content_1, content_2)).replace('lsttb', tab)

def no_supflu_0(inp):
    return (inp + '.').rstrip('0').rstrip('.')

def calc_rank(prec, size):
    return math.log2(size / prec)

path = ""

default_map = parse_file(os.path.join(path, "map", "default.map"))

provnumber = int(default_map["max_provinces"])

climate = parse_file(os.path.join(path, "map", "climate.txt"))

provinces = [p for p in range(1,provnumber) if (str(p) not in default_map["only_used_for_random"] and not str(p) in default_map["lakes"] and not str(p) in default_map["sea_starts"] and not str(p) in climate['impassable'])]


prec = 1
start = 1
end = len(provinces)
print (end)

rank = math.ceil(calc_rank(prec, end - start + 1))

trig = 'check_key = { lhs = S_ID value = %s }'
content = '%s = { save_event_target_as = GetProvOut }'

with open('output.txt', 'w') as f:
    f.write(make_binary_tree('', rank, start, end, trig, content))
