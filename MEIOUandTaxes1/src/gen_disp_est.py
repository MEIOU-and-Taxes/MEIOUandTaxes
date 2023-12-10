def get_next(inp, step, tick):
    inp[2] += step

    for ind in range(len(inp) - 1, 0, -1):
        if inp[ind] > tick:
            inp[ind - 1] += step
            inp[ind] = 0

    return inp

string = ''
form = '''disp_ss_%s =
{
	icon = 8

	color = { %s %s %s }

	# Is estate kept in control of province on conquest?
	keep_on_conquest = no
	
	min_territory = 0
	min_provinces_to_want_territory = 999

	# If true, country will get estate
	trigger = {
		always = no
	}

	# If true, province can be granted to estate
	province_trigger = {
		always = no
	}

	# Min autonomy in estate provinces
	min_autonomy = 0
	
	country_modifier_happy = {}
	country_modifier_neutral = {}
	country_modifier_angry = {}
	
	# These do not scale, but only applied in provinces owned by the estate
	province_modifier_happy = {
	}
	province_modifier_neutral = {
	}
	province_modifier_angry = {
	}
}
'''

rgb = [0, 0, 0]

for itr in range(1, 101):
    get_next(rgb, 40, 256)
    
    string += form % (itr, rgb[0], rgb[1], rgb[2])

form = 'else_if = { limit = { is_key_equal = { lhs = iter value = %s } } every_owned_province = { limit = { PartOfRank1 = { Compare = event_target:Prov } } set_estate = disp_ss_%s } }\n'

for itr in range(1, 101):
    string += form % (itr, itr)

with open('output.txt', 'w') as f:
    f.write(string)
