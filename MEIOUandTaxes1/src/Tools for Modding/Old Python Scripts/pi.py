import glob, sys

def pi_mtth_lack(file_loc):
    with open(file_loc, 'r', encoding='ISO-8859-1') as f1:
        text = f1.readlines()

        file_name = file_loc[file_loc.find('\\') + 1:]

        event = False

        for ind in range(len(text)):
            line = text[ind]
            
            if '#' in line:
                line_temp = str(line)[:line.find('#')]
            else:
                line_temp = str(line)

            if not event and not 'namespace' in line_temp and '_event' in line_temp:
                event = True
                mtth = False
                eid = False
                t_only = False

                bracket = 0
                eid_str = ''

            if event:
                for char in line_temp:
                    if char == '{':
                        bracket += 1
                    elif char == '}':
                        bracket -= 1

                if not eid and 'id' in line_temp:
                    eid = True

                    eid_str = line_temp[line_temp.find('id') + 3:].strip('= \n\t')

                if 'is_triggered_only' in line_temp \
                and 'yes' in line_temp[line_temp.find('is_triggered_only') + 17:].lstrip(' =')[:3]:
                    t_only = True

                if 'mean_time_to_happen' in line_temp:
                    mtth = True

                if bracket == 0:
                    event = False

                    if not (mtth or t_only):
                        sys.stdout.write(file_name + ', ' + eid_str + '\n')              

def pi_mtth(file_loc):
    with open(file_loc, 'r', encoding='ISO-8859-1') as f1:
        text = f1.readlines()

        file_name = file_loc[file_loc.find('\\') + 1:]

        mtth = False
        
        for ind in range(len(text)):
            line = text[ind]
            
            if '#' in line:
                line_temp = str(line)[:line.find('#')]
            else:
                line_temp = str(line)

            if not mtth and 'mean_time_to_happen' in line_temp:
                mtth = True

                months = False
                days = False
                proceed = False

            if mtth:
                if 'years' in line_temp:
                    mtth = False
                else:
                    if 'months' in line_temp:
                        proceed = True
                        months = True
                        letters = 7
                    elif 'days' in line_temp:
                        proceed = True
                        days = True
                        letters = 5

                    if proceed:
                        mtth = False
                        
                        if months:
                            loc_start = line_temp.find('months')
                        else:
                            loc_start = line_temp.find('days')

                        num = 0
                        loc_end = int(loc_start + letters)
                        
                        num_found = False

                        for char in line_temp[loc_start + letters:]:
                            loc_end += 1
                            
                            if 48 <= ord(char) <= 57:
                                num *= 10
                                num += int(char)

                                if not num_found:
                                    num_found = True
                            elif num_found:
                                break

                        large_enough = False

                        to_months = False

                        if months:
                            if num >= 12:
                                num = int(num / 12)

                                large_enough = True
                        else:
                            if num >= 365:
                                num = int(num / 365)

                                large_enough = True
                            elif num >= 30:
                                to_months = True

                                num = int(num / 30)

                                large_enough = True

                        if large_enough:
                            if to_months:
                                statement = 'months = '
                            else:
                                statement = 'years = '

                            statement += str(num)

                            text[ind] = line[:loc_start] + statement + line[loc_end:] + '\n'
                        elif days:
                            sys.stdout.write(file_name + ', ' + str(ind) + '\n')        

        with open(file_loc, 'w', encoding='ISO-8859-1') as f2:
            f2.writelines(text)

files = glob.glob('events\*.txt')

for file in files:
    pi_mtth_lack(file)
    pi_mtth(file)

input()
