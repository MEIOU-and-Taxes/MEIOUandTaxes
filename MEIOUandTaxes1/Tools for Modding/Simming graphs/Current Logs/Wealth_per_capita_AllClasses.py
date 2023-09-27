from matplotlib import pyplot as plt
import pandas as pd

def get_data(t, i):
    lst = []
    loc = 0

    while True:
        loc = t.find(i, loc)

        if loc != -1:
            end = t.find('\n', loc)
            lst.append(float(t[loc:end].strip().split(':')[1].strip().split("£")[-1]))
            loc = end
        else:
            break

    return lst

import os
def read_and_concatenate_old_logs(directory='.'):
    concatenated_text = ''
    for file_name in sorted(os.listdir(directory)):
        if file_name.startswith('game_') and file_name.endswith('.log') and file_name != 'game.log':
            with open(file_name, 'r') as f:
                concatenated_text += f.read()
    return concatenated_text

if __name__ == '__main__':
    with open('game.log') as f:
        t = read_and_concatenate_old_logs()
        t += f.read()
        
        wealth_SF = get_data(t, 'Peasant Wealth')
        wealth_NM = get_data(t, 'Nomad Wealth')
        wealth_RE = get_data(t, 'Resident Wealth')
        wealth_NO = get_data(t, 'Noble Wealth')
        wealth_BG = get_data(t, 'Burgher Wealth')
        wealth_CL = get_data(t, 'Clergy Wealth')
        SF = get_data(t, 'Peasant Pop Total')
        NM = get_data(t, 'Nomads Pop Total')
        RE = get_data(t, 'Residents Pop Total')
        NO = get_data(t, 'Nobles Pop Total')
        BG = get_data(t, 'Burghers Pop Total')
        CL = get_data(t, 'Clergy Pop Total')

        SF_wpc = [a / b for a, b in zip(wealth_SF, SF)]
        NM_wpc = [a / b for a, b in zip(wealth_NM, NM)]
        RE_wpc = [a / b for a, b in zip(wealth_RE, RE)]
        NO_wpc = [a / b for a, b in zip(wealth_NO, NO)]
        BG_wpc = [a / b for a, b in zip(wealth_BG, BG)]
        CL_wpc = [a / b for a, b in zip(wealth_CL, CL)]
        itr = range(1, len(SF_wpc) + 1)

        plt.title("Wealth per Capita per Class")
        plt.plot(itr, SF_wpc, label="Peasants Wealth p.c.")
        plt.plot(itr, NM_wpc, label="Nomads Wealth p.c.")
        plt.plot(itr, RE_wpc, label="Residents Wealth p.c.")
        plt.plot(itr, NO_wpc, label="Nobles Wealth p.c.")
        plt.plot(itr, BG_wpc, label="Burghers Wealth p.c.")
        plt.plot(itr, CL_wpc, label="Clergy Wealth p.c.")

        plt.legend(loc=2, ncol=2)

        plt.show()
