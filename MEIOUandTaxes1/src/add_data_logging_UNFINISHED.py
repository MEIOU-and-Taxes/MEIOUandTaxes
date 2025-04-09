data = ["ID", "ID_Region", "Class_Wealth"]

# eventformat = """country_event = {
#     id = POP_Census.995
#     title = no_localisation
#     desc = no_localisation
# 	picture = MEIOU_AND_TAXES_eventPicture

#     hidden = yes
#     is_triggered_only = yes
# 	trigger = {
# 		has_global_flag = POP_Census.995
# 	}

# 	immediate = {
# 		%s
# 		every_country = {
# 		    limit = {
# 		    	has_country_flag = POP_Census.995
# 		    }
# 		    %s
# 		}
# 		every_province = {
# 		    limit = {
# 		    	has_province_flag = POP_Census.995
# 		    }
# 		    %s
# 		}
# 	}
# 	option = {
# 		name = EXIT
# 	}
# }
# """ % (title, country, province)
# log = "log = \"%s\"" % (data)

if __name__ == "__main__":
    with open("keys.txt", "r") as keyfile:
        for key in keyfile.readlines():
            key = key.rstrip("\n").split(" ")
            if key[0] in data:
                data = [key[2] if x == key[0] else x for x in data]



    print("Added data logging to files")
    input()