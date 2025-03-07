# by KJH, Phlopsi & JF

import os

comment = """########################################
# This file was autogenerated by {}
# Do not edit this file directly!
########################################
""".format( os.path.basename( __file__ ) )

def set_dct(dct, path):
    with open(path) as f:
        for line in f.readlines():
            line = line.strip(' \n\t').replace("  ", " ").split(" ")
            if len(line) == 1:
                dct[line[0]] = ""
            else:
                dct[line[0]] = line[1]

def set_scopes(scopes, path):
    with open(path) as f:
        for line in f.readlines():
            line = line.strip(' \n\t')
            scopes.append("event_target:" + line)
            scopes.sort()

def get_key(val):
    import string
    
    table = list(string.ascii_lowercase)
    
    out = ''
    
    while val >= len(table):
        out = table[val % len(table)] + out

        val //= len(table)
        val -= 1

    out = table[val] + out

    return out

def set_key(dct):
    count = 702
    
    for var in dct:
        if dct[var] != "":
            width = dct[var].split(':')
            if width[0][0].isdigit() == True:
                width[0] = "x" + width[0]
            x = int("".join(width[0][1:])) - 1
            if x < 0:
                x = 0
            dct[var] = [get_key(count), x, int(width[1]), width[0][0]]
        else:
            dct[var] = [get_key(count)]
        count += 1

def gen_scripts(tmplt, dct, out, encoding=None):
    txt = ""
    with open(out, 'w', encoding=encoding, newline = '\n') as f:
        for var in dct:
            txt += tmplt.replace('%s', var).replace('%d', dct[var][0])

        f.write(comment)
        f.write(txt)
def gen_script_core(txt, out, encoding=None):
    with open(out, 'w', encoding=encoding, newline = '\n') as f:
        f.write(comment)
        f.write(txt)

def gen_customloc(txt, tmpltA, tmpltB, tmplt1, tmplt1H, tmplt2, tmplt2H, tmpltN, dct, out, encoding=None):
    with open(out, 'w', encoding=encoding, newline = '\n') as f:
        for var in dct:
            if len(dct[var]) > 1:
                if dct[var][3] != '+' and dct[var][3] != '-':
                    txt += tmpltN.replace('%s', var).replace('%d', dct[var][0])
                
                if dct[var][1] > 0:
                    text = tmplt1
                    for x in range(dct[var][1], 0, -1):
                        text = text.replace("%H", tmplt1H.replace("%a", str(dct[var][1] + 1 - x)).replace("%b", str(pow(10, x))))
                    text = text.replace("%H", "")
                    txt += text.replace('%s', var).replace('%d', dct[var][0])
                
                if dct[var][2] > 0:
                    text = tmplt2
                    i = 3
                    for x in range(dct[var][2], 0, -1):
                        text = text.replace("%H", tmplt2H.replace("%a", str(dct[var][2]) + str(x)).replace("%b", str(pow(10, i))))
                        i -= 1
                    text = text.replace("%H", "")
                    txt += text.replace('%s', var).replace('%d', dct[var][0])
                
                if dct[var][3] == '+':
                    text = tmpltA.replace('%N', '0')
                else:
                    text = tmpltA.replace('%N', 'N')
                txt += text.replace('%s', var).replace('%d', dct[var][0]).replace('%a', str(dct[var][1]) + str(dct[var][2]))
            
            else:
                txt += tmpltB.replace('%s', var).replace('%d', dct[var][0])

        f.write(comment)
        f.write(txt)

def gen_loc(txt, tmplt, tmpltH1, tmpltH2, tmpltN, dct, out, encoding=None):
    with open(out, 'w', encoding=encoding, newline = '\n') as f:
        for var in dct:
            if len(dct[var]) > 1:
                text = tmplt
                if dct[var][3] != '+' and dct[var][3] != '-':
                    text = text.replace("%N", tmpltN)
                else:
                    text = text.replace("%N", "")
                if dct[var][1] > 0:
                    text = text.replace("%H1", tmpltH1)
                if dct[var][2] > 0:
                    text = text.replace("%H2", tmpltH2)
                txt += text.replace('%s', var).replace('%S', var.replace('_', ' ')).replace('%d', dct[var][0]).replace("%H1", "").replace('%H2', "").replace("%N", "")
            else:
                txt += tmplt.replace('%s', var).replace('%S', var.replace('_', ' ')).replace('%d', dct[var][0]).replace("%H1", "").replace('%H2', "").replace("%N", "")

        f.write(comment)
        f.write(txt)

def compress(txt):
    return (' '.join(txt.replace('\t','').replace('\n',' ').split()))+'\n'

def compress2(txt):
    return txt.replace('\t','').replace('  ','').replace('\n','')+'\n'

def compressH(txt):
    return ' ' + (' '.join(txt.replace('\t','').replace('\n',' ').split()))

dont = ['keys.txt', '00-scripts_core.txt', '00-scripts.txt', '00-triggers_core.txt', '00-triggers.txt',
        'vars.txt', '00-locs_l_english.yml', '00-locs.txt']

effect = """set_key = {
[[which]
    set_key_lhs_$lhs$ = {
        which = $which$
    }
]
[[value]
    set_key_value_$lhs$ = {
        value = $value$
    }
]
}
change_key = {
[[which]
    change_key_lhs_$lhs$ = {
        which = $which$
    }
]
[[value]
    change_key_value_$lhs$ = {
        value = $value$
    }
]
}
subtract_key = {
[[which]
    subtract_key_lhs_$lhs$ = {
        which = $which$
    }
]
[[value]
    subtract_key_value_$lhs$ = {
        value = $value$
    }
]
}
multiply_key = {
[[which]
    multiply_key_lhs_$lhs$ = {
        which = $which$
    }
]
[[value]
    multiply_key_value_$lhs$ = {
        value = $value$
    }
]
}
divide_key = {
[[which]
    divide_key_lhs_$lhs$ = {
        which = $which$
    }
]
[[value]
    divide_key_value_$lhs$ = {
        value = $value$
    }
]
}
export_to_key = {
    export_to_variable = {
        which = export
        value = $value$
[[who]  who = $who$ ]
[[with] with = $with$ ]
    }
    set_key_from_var = { key = $lhs$ var = export }
}
set_var_from_key = {
    set_key_rhs_$key$ = {
        lhs = $var$
    }
}
set_key_from_var = {
    set_key_which_$key$ = {
        which = $var$
    }
}
change_var_by_key = {
    change_key_rhs_$key$ = {
        lhs = $var$
    }
}
subtract_var_by_key = {
    subtract_key_rhs_$key$ = {
        lhs = $var$
    }
}
multiply_var_by_key = {
    multiply_key_rhs_$key$ = {
        lhs = $var$
    }
}
divide_var_by_key = {
    divide_key_rhs_$key$ = {
        lhs = $var$
    }
}
change_key_by_var = {
    change_key_lhs_$key$ = {
        which = $var$
    }
}
subtract_key_by_var = {
    subtract_key_lhs_$key$ = {
        which = $var$
    }
}
multiply_key_by_var = {
    multiply_key_lhs_$key$ = {
        which = $var$
    }
}
divide_key_by_var = {
    divide_key_lhs_$key$ = {
        which = $var$
    }
}
export_key_to_var = {
    export_to_variable = {
        which = $var$
        value = 0
    }
    change_var_by_key = {
        var = $var$
        key = $key$
    }
}
"""
effect = compress(effect)

tmplt_effect_scope = """set_key_rhs_%s={
    _b={d=%s l=$lhs$}
}
change_key_rhs_%s={
    _f={d=%s l=$lhs$}
}
subtract_key_rhs_%s={
    _i={d=%s l=$lhs$}
}
multiply_key_rhs_%s={
    _o={d=%s l=$lhs$}
}
divide_key_rhs_%s={
    _l={d=%s l=$lhs$}
}
"""
tmplt_effect_scope = compress2(tmplt_effect_scope)

tmplt_effect = """set_key_lhs_%s={
    _a={d=%d w=$which$}
}
set_key_rhs_%s={
    _b={d=%d l=$lhs$}
}
set_key_value_%s={
    _c={d=%d v=$value$}
}
set_key_which_%s={
    _d={d=%d w=$which$}
}
change_key_lhs_%s={
    _e={d=%d w=$which$}
}
change_key_rhs_%s={
    _f={d=%d l=$lhs$}
}
change_key_value_%s={
    _g={d=%d v=$value$}
}
subtract_key_lhs_%s={
    _h={d=%d w=$which$}
}
subtract_key_rhs_%s={
    _i={d=%d l=$lhs$}
}
subtract_key_value_%s={
    _j={d=%d v=$value$}
}
divide_key_lhs_%s={
    _k={d=%d w=$which$}
}
divide_key_rhs_%s={
    _l={d=%d l=$lhs$}
}
divide_key_value_%s={
    _m={d=%d v=$value$}
}
multiply_key_lhs_%s={
    _n={d=%d w=$which$}
}
multiply_key_rhs_%s={
    _o={d=%d l=$lhs$}
}
multiply_key_value_%s={
    _p={d=%d v=$value$}
}
"""
tmplt_effect = compress2(tmplt_effect)

trigger = """check_key = {
[[which]
    check_key_lhs_$lhs$ = {
        which = $which$
    }
]
[[value]
    check_key_value_$lhs$ = {
        value = $value$
    }
]
}
is_key_equal = {
[[which]
    is_key_equal_lhs_$lhs$ = {
        which = $which$
    }
]
[[value]
    is_key_equal_value_$lhs$ = {
        value = $value$
    }
]
}
check_var_by_key = {
    check_key_rhs_$key$ = {
        lhs = $var$
    }
}
is_var_equal_to_key = {
    is_key_equal_rhs_$key$ = {
        lhs = $var$
    }
}
"""
trigger = compress(trigger)

tmplt_trigger_scope = """check_key_rhs_%s={
    _r={d=%s l=$lhs$}
}
is_key_equal_rhs_%s={
    _u={d=%s l=$lhs$}
}
"""
tmplt_trigger_scope = compress2(tmplt_trigger_scope)

tmplt_trigger = """check_key_lhs_%s={
    _q={d=%d w=$which$}
}
check_key_rhs_%s={
    _r={d=%d l=$lhs$}
}
check_key_value_%s={
    _s={d=%d v=$value$}
}
is_key_equal_lhs_%s={
    _t={d=%d w=$which$}
}
is_key_equal_rhs_%s={
    _u={d=%d l=$lhs$}
}
is_key_equal_value_%s={
    _w={d=%d v=$value$}
}
"""
tmplt_trigger = compress2(tmplt_trigger)

loc = '''l_english:
 GV_0: "0"
 GV_N: "£5px£"
 GVL_0: ""
 GVL_1: "£7px£"
 GVL_2: "£14px£"
 GVL_3: "£21px£"
 GVL_4: "£28px£"
 GVL_5: "£35px£"
 GVL_6: "£42px£"
 GVR_0: ""
 GVR_11: ".0"
 GVR_21: "0"
 GVR_22: ".00"
 GVR_31: "0"
 GVR_32: "00"
 GVR_33: ".000"
 GV0_00: "0"
 GV0_01: "0.0"
 GV0_02: "0.00"
 GV0_03: "0.000"
 GV0_10: "£7px£0"
 GV0_11: "£7px£0.0"
 GV0_12: "£7px£0.00"
 GV0_13: "£7px£0.000"
 GV0_20: "£14px£0"
 GV0_21: "£14px£0.0"
 GV0_22: "£14px£0.00"
 GV0_23: "£14px£0.000"
 GV0_30: "£21px£0"
 GV0_31: "£21px£0.0"
 GV0_32: "£21px£0.00"
 GV0_33: "£21px£0.000"
 GV0_40: "£28px£0"
 GV0_41: "£28px£0.0"
 GV0_42: "£28px£0.00"
 GV0_43: "£28px£0.000"
 GV0_50: "£35px£0"
 GV0_51: "£35px£0.0"
 GV0_52: "£35px£0.00"
 GV0_53: "£35px£0.000"
 GV0_60: "£42px£0"
 GV0_61: "£42px£0.0"
 GV0_62: "£42px£0.00"
 GV0_63: "£42px£0.000"
 GVN_00: "£5px£0"
 GVN_01: "£5px£0.0"
 GVN_02: "£5px£0.00"
 GVN_03: "£5px£0.000"
 GVN_10: "£12px£0"
 GVN_11: "£12px£0.0"
 GVN_12: "£12px£0.00"
 GVN_13: "£12px£0.000"
 GVN_20: "£19px£0"
 GVN_21: "£19px£0.0"
 GVN_22: "£19px£0.00"
 GVN_23: "£19px£0.000"
 GVN_30: "£26px£0"
 GVN_31: "£26px£0.0"
 GVN_32: "£26px£0.00"
 GVN_33: "£26px£0.000"
 GVN_40: "£33px£0"
 GVN_41: "£33px£0.0"
 GVN_42: "£33px£0.00"
 GVN_43: "£33px£0.000"
 GVN_50: "£40px£0"
 GVN_51: "£40px£0.0"
 GVN_52: "£40px£0.00"
 GVN_53: "£40px£0.000"
 GVN_60: "£47px£0"
 GVN_61: "£47px£0.0"
 GVN_62: "£47px£0.00"
 GVN_63: "£47px£0.000"
'''
tmplt_loc = ' GV_%s: "%N%H1[This.%d.GetValue]%H2"\n %d: "%S"\n'
tmpltN_loc = '[GVN_%s]'
tmpltH1_loc = '[GVL_%s]'
tmpltH2_loc = '[GVR_%s]'

locc = ''
tmpltA_locc = """defined_text = {
    name = GV_%s
    random = no
    text = {
        trigger = {
            NOT = { is_variable_equal = { which = %d value = 0 } }
        }
        localisation_key = GV_%s
    }
    text = {
        localisation_key = GV%N_%a
    }
}"""
tmpltB_locc = """defined_text = {
    name = GV_%s
    random = no
    text = {
        trigger = {
            NOT = { is_variable_equal = { which = %d value = 0 } }
        }
        localisation_key = GV_%s
    }
    text = {
        localisation_key = GV_0
    }
}"""

tmpltN_locc = """defined_text = {
    name = GVN_%s
    random = no
    text = {
        localisation_key = GV_N
        trigger = {
            check_variable = { which = %d value = 0 }
        }
    }
}
"""

tmplt1_locc = """
defined_text = {
    name = GVL_%s
    random = no
    text = {
        localisation_key = GVL_0%H
    }
}
"""
tmplt1H_locc = """
        trigger = {
            OR = {
                check_variable = { which = %d value = %b }
                NOT = { check_variable = { which = %d value = -%b } }
            }
        }
    }
    text = {
        localisation_key = GVL_%a%H"""

tmplt2_locc = """defined_text = {
    name = GVR_%s
    random = no%H
    text = {
        localisation_key = GVR_0
    }
}
"""
tmplt2H_locc = """
    text = {
        localisation_key = GVR_%a
        trigger = {
            variable_arithmetic_trigger = {
                export_to_variable = { which = temp value = religion }
                subtract_variable = { which = temp which = temp }
                change_variable = { which = temp which = %d }
                divide_variable = { which = temp value = %b }
                multiply_variable = { which = temp value = %b }
                subtract_variable = { which = temp which = %d }
                is_variable_equal = { which = temp value = 0 }
            }
        }
    }%H"""

# tmpltA_locc = compress(tmpltA_locc)
# tmpltB_locc = compress(tmpltB_locc)
# tmplt1_locc = compressH(tmplt1_locc)
# tmplt1H_locc = compressH(tmplt1H_locc)
# tmplt2_locc = compressH(tmplt2_locc)
# tmplt2H_locc = compressH(tmplt2H_locc)
# tmpltN_locc = compressH(tmpltN_locc)

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    
    
    dct = dict()
    scopes = ["ROOT", "FROM", "THIS", "PREV", "emperor", "EMPEROR", "owner", "OWNER", "capital", "CAPITAL", "AAA"]

    set_scopes(scopes, 'event_targets.txt')
    set_dct(dct, 'vars.txt')
    set_key(dct)

    for scope in scopes:
        trigger += tmplt_trigger_scope.replace('%s', scope)
        effect += tmplt_effect_scope.replace('%s', scope)

    gen_scripts(tmplt_effect, dct, os.path.join('common', 'scripted_effects', '00-scripts.txt'))
    gen_script_core(effect, os.path.join('common', 'scripted_effects', '00-scripts_core.txt'))
    gen_scripts(tmplt_trigger, dct, os.path.join('common', 'scripted_triggers', '00-triggers.txt'))
    gen_script_core(trigger, os.path.join('common', 'scripted_triggers', '00-triggers_core.txt'))
    gen_loc(loc, tmplt_loc, tmpltH1_loc, tmpltH2_loc, tmpltN_loc, dct, os.path.join('localisation', '00-locs_l_english.yml'), encoding='utf-8-sig')
    gen_customloc(locc, tmpltA_locc, tmpltB_locc, tmplt1_locc, tmplt1H_locc, tmplt2_locc, tmplt2H_locc, tmpltN_locc, dct, os.path.join('customizable_localization', '00-locs.txt'))

    string = ''

    for i in dct:
        string += '%s : %s\n' % (i, dct[i][0])

    with open('keys.txt', 'w', newline = '\n') as f:
        f.write(string)
