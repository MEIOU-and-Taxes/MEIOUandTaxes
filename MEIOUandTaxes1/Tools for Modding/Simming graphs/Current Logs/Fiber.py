from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

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
        
        Fiberp = np.array(get_data(t, 'Fiber Production'))
        Fiberd = np.array(get_data(t, 'Fiber Demand'))
        Fibere = np.array(get_data(t, 'Fiber DirectBuy'))
        Fiberf = Fiberd + Fibere
        Fiberj = Fiberp + Fibere
        itr = range(1, len(Fiberp) + 1)

        plt.plot(itr, Fiberp, label="Production")
        plt.plot(itr, Fiberd, label="Market Demand")
        plt.plot(itr, Fibere, label="Direct Buy")
        plt.plot(itr, Fiberf, label="Total Demand")
        plt.plot(itr, Fiberj, label="Total Production")

        plt.legend(loc=2, ncol=2)

        plt.show()
