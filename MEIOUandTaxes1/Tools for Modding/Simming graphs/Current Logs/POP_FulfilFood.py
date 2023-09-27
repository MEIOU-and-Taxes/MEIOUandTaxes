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
        
        #Class = get_data(t, 'Class Pop Total')
        SF = get_data(t, 'Fulfil SF Food')
        NM = get_data(t, 'Fulfil NM Food')
        RE = get_data(t, 'Fulfil RE Food')
        NO = get_data(t, 'Fulfil NO Food')
        BG = get_data(t, 'Fulfil BG Food')
        CL = get_data(t, 'Fulfil CL Food')
        SFD = get_data(t, 'Fulfil SF Direct Food')
        NMD = get_data(t, 'Fulfil NM Direct Food')
        NOD = get_data(t, 'Fulfil NO Direct Food')
        CLD = get_data(t, 'Fulfil CL Direct Food')
        itr = range(1, len(SF) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, SF, label="Peasants Total")
        plt.plot(itr, NM, label="Nomads Total")
        plt.plot(itr, NO, label="Nobles Total")
        plt.plot(itr, CL, label="Clergy Total")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, SFD, label="Peasants Direct")
        plt.plot(itr, NMD, label="Nomads Direct")
        plt.plot(itr, NOD, label="Nobles Direct")
        plt.plot(itr, CLD, label="Clergy Direct")

        plt.legend(loc=2, ncol=2)

        plt.show()
