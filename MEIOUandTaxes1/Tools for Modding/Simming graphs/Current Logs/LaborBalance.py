from matplotlib import pyplot as plt
import pandas as pd

def get_data(t, i):
    lst = []
    loc = 0

    while True:
        loc = t.find(i, loc)

        if loc != -1:
            end = t.find('\n', loc)
            lst.append(float(t[loc:end].strip().split(':')[1].strip()))
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
        
        SF = get_data(t, 'Labor Funded R')
        NM = get_data(t, 'Labor Funded NM')
        RE = get_data(t, 'Labor Funded UL')
        NO = get_data(t, 'Labor Funded NO')
        BG = get_data(t, 'Labor Funded BG')
        CL = get_data(t, 'Labor Funded CL')
        BU = get_data(t, 'Labor Funded LT')
        SF2 = get_data(t, 'Labor Cost R')
        NM2 = get_data(t, 'Labor Cost NM')
        RE2 = get_data(t, 'Labor Cost UL')
        NO2 = get_data(t, 'Labor Cost NO')
        BG2 = get_data(t, 'Labor Cost BG')
        CL2 = get_data(t, 'Labor Cost CL')
        BU2 = get_data(t, 'Labor Cost LT')
        itr = range(1, len(SF) + 1)
        SF = [SF[i]-SF2[i] for i in range(len(SF))]
        NM = [NM[i]-NM2[i] for i in range(len(NM))]
        RE = [RE[i]-RE2[i] for i in range(len(RE))]
        NO = [NO[i]-NO2[i] for i in range(len(NO))]
        BG = [BG[i]-BG2[i] for i in range(len(BG))]
        CL = [CL[i]-CL2[i] for i in range(len(CL))]
        BU = [BU[i]-BU2[i] for i in range(len(BU))]

        plt.plot(itr, SF, label="Peasants")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, CL, label="Clergy")
        plt.plot(itr, BU, label="State")

        plt.legend(loc=2, ncol=2)

        plt.show()
