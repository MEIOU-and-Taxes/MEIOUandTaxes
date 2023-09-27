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
        
        #Class = get_data(t, 'Class Pop')
        SF = get_data(t, 'Fulfil SF Comfort')
        NM = get_data(t, 'Fulfil NM Comfort')
        RE = get_data(t, 'Fulfil RE Comfort')
        NO = get_data(t, 'Fulfil NO Comfort')
        BG = get_data(t, 'Fulfil BG Comfort')
        CL = get_data(t, 'Fulfil CL Comfort')
        itr = range(1, len(SF) + 1)

        #plt.plot(itr, Class, label="Total")
        plt.plot(itr, SF, label="Peasants")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, CL, label="Clergy")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, BG, label="Burghers")
        plt.legend(loc=2, ncol=2)

        plt.show()
