with open('out.txt', 'w') as f:
    t = ''

    with open('keys.txt') as ff:
        for line in ff.readlines():
            t += 'set_variable = { which = %s $type$ = $command$ }\n' % line.split(':')[1].strip()

    f.write(t)
