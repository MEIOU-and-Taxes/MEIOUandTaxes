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
        
        Fuel1 = get_data(t, 'Paris Fuel Price')
        Fuel2 = get_data(t, 'Moscow Fuel Price')
        Fuel3 = get_data(t, 'Cairo Fuel Price')
        Fuel4 = get_data(t, 'Gao Fuel Price')
        Fuel5 = get_data(t, 'Mogadishu Fuel Price')
        Fuel6 = get_data(t, 'Delhi Fuel Price')
        Fuel7 = get_data(t, 'Malacca Fuel Price')
        Fuel8 = get_data(t, 'Nanking Fuel Price')
        Fuel9 = get_data(t, 'Mexico Fuel Price')
        Fuel10 = get_data(t, 'Cusco Fuel Price')
        itr = range(1, len(Fuel1) + 1)

        plt.plot(itr, Fuel1, label="Paris")
        plt.plot(itr, Fuel2, label="Moscow")
        plt.plot(itr, Fuel3, label="Cairo")
        plt.plot(itr, Fuel4, label="Gao")
        plt.plot(itr, Fuel5, label="Mogadishu")
        plt.plot(itr, Fuel6, label="Delhi")
        plt.plot(itr, Fuel7, label="Malacca")
        plt.plot(itr, Fuel8, label="Nanking")
        plt.plot(itr, Fuel9, label="Mexico")
        plt.plot(itr, Fuel10, label="Cusco")

        plt.legend(loc=2, ncol=2)

        plt.show()
