with open('events\\00-POP_Init.txt') as f:
    txt = f.read()

    txt = txt.replace('_v=', 'set_variable=')
    txt = txt.replace('{v=', '{which=')
    txt = txt.replace(' n=', ' value=')

    txt = txt.replace('} _pf={f=', ' set_province_flag=')
    txt = txt.replace('_pf={f=', '{set_province_flag=')

    prev = 0

    while True:
        start = txt.find('{set_province_flag=', prev)

        if start + 1:
            print('a', start / len(txt))
            
            block = txt[start:txt.find('}', start) + 1]

            txt = txt.replace(block, block[1:-1])

            prev = start + len(block) - 2
        else:
            break

    txt = txt.replace('} _cf={f=', ' set_country_flag=')
    txt = txt.replace('_cf={f=', '{set_country_flag=')

    prev = 0

    while True:
        start = txt.find('{set_country_flag=', prev)

        if start + 1:
            print('b', start / len(txt))
            
            block = txt[start:txt.find('}', start) + 1]

            txt = txt.replace(block, block[1:-1])

            prev = start + len(block) - 2
        else:
            break

    txt = txt.replace('_pm={m=', 'add_province_modifier={duration=-1 name=')
    txt = txt.replace('_pmh={m=', 'add_province_modifier={duration=-1 hidden=yes name=')
    txt = txt.replace('_ppm={m=', 'add_permanent_province_modifier={duration=-1 name=')
    txt = txt.replace('_ppmh={m=', 'add_permanent_province_modifier={duration=-1 hidden=yes name=')
    txt = txt.replace('_cm={m=', 'add_country_modifier={duration=-1 name=')
    txt = txt.replace('_cmh={m=', 'add_country_modifier={duration=-1 hidden=yes name=')
    
    with open('test.txt', 'w') as ff:
        ff.write(txt)
