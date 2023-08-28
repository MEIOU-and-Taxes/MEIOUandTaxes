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

def btree(lst, form, body):
    if not len(lst):
        return ''
    elif len(lst) == 1:
        return body % lst[0]
    else:
        return form % (lst[int(len(lst)/2)],
                       btree(lst[int(len(lst)/2):], form.replace('\n', '\n\t'), body),
                       btree(lst[:int(len(lst)/2)], form.replace('\n', '\n\t'), body))
        
if __name__ == "__main__":
        cond = 'check_key = { lhs = $var$ value = %s }'
        body = 'add_country_modifier = { name = $type$_penalty_%s duration = 364 }'
        form = 'if = {\n\tlimit = {\n\t\t%s\n\t}\n\t%s\n}\nelse = {\n\t%s\n}' % (cond, '%s', '%s')

        with open('output.txt', 'w') as f:
            for i in range(5, 100, 3):
                f.write(f'''morale_penalty_{i} = {{
    land_morale = -{round((i / 200), 3)}
    reinforce_speed = -{round(i/120,3)}\n}}\n''')

            for i in range(5, 100, 3):
                f.write(f'''discipline_penalty_{i} = {{
    fire_damage = -{round((i / 150),3)}
    shock_damage = -{round((i / 150), 3)}
    siege_ability = -{round((i / 100), 3)}\n}}\n''')

                for i in range(5, 100, 3):
                    f.write(f'''knowledge_penalty_{i} = {{
	cavalry_flanking = -{round((i / 110), 3)}
	backrow_artillery_damage = -{round((i / 110), 3)}\n}}\n''')
            iterator = 0
            for i in range(5, 100, 3):
                iterator = iterator+1
                f.write(f'''knowledge_penalty_{i}: "Insufficiently supplied armies (Knowledge). \\nTier {33-iterator}"\n''')


