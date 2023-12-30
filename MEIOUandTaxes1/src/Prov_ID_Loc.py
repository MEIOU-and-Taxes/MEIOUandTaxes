import math, sys

f = open('prov_id.txt','r')
ids = f.readlines()
f.close()

f = open('prov_names.txt','r',encoding='utf-8-sig')
prov_names = f.readlines()
f.close()


sys.stdout.write('Variable Name for Checking in Custom Localisation:\n')

var_name = input()

cust_localisation_main = """defined_text = {
        name = Prov_ID_Loc_%variable

%texts

}
"""

cust_localisation_tmpl = """
        text = {
                localisation_key = Prov%id

                trigger = {
                        is_key_equal = { lhs = %variable value = %id }
                }
        }
"""

localisation_template = ''' Prov%id: "%name"
'''

localisation_buffer = ""
localisation_buffer2 = ""
localisation_buffer3 = ""
modifier_loc_buffer = ""
custom_localisation_buffer = ""
custom_localisation_buffer2 = ""
custom_localisation_buffer3 = ""
effect_buffer = ""


counter = 0
# Iterate over each column
while counter < len(ids):
        custom_localisation_buffer += cust_localisation_tmpl.replace('%id',ids[counter].replace('\n',''))
        
        localisation_buffer += localisation_template.replace('%id',ids[counter].replace('\n',''))
        localisation_buffer = localisation_buffer.replace('%name',prov_names[counter].replace('\n',''))
        
        counter += 1



custom_localisation_buffer = custom_localisation_buffer.replace('%variable',var_name)
custom_localisation_buffer2 = cust_localisation_main.replace('%texts',custom_localisation_buffer)
custom_localisation_buffer2 = custom_localisation_buffer2.replace('%variable',var_name)


localisation_buffer2 = """l_english:
"""
localisation_buffer2 += localisation_buffer

f = open('localisation\\DISP-Prov_ID_Loc_l_english.yml','w',encoding='utf-8-sig')
f.write(localisation_buffer2)
f.close

f = open('customizable_localization\\DISP-Prov_ID_Loc'+var_name+'.txt','w')
f.write(custom_localisation_buffer2)
f.close

print("Script successfully executed")
