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
        
        Raw1 = get_data(t, 'Paris Raw Material Price')
        Raw2 = get_data(t, 'Moscow Raw Material Price')
        Raw3 = get_data(t, 'Cairo Raw Material Price')
        Raw4 = get_data(t, 'Gao Raw Material Price')
        Raw5 = get_data(t, 'Mogadishu Raw Material Price')
        Raw6 = get_data(t, 'Delhi Raw Material Price')
        Raw7 = get_data(t, 'Malacca Raw Material Price')
        Raw8 = get_data(t, 'Nanking Raw Material Price')
        Raw9 = get_data(t, 'Mexico Raw Material Price')
        Raw10 = get_data(t, 'Cusco Raw Material Price')
        itr = range(1, len(Raw1) + 1)

        plt.plot(itr, Raw1, label="Paris")
        plt.plot(itr, Raw2, label="Moscow")
        plt.plot(itr, Raw3, label="Cairo")
        plt.plot(itr, Raw4, label="Gao")
        plt.plot(itr, Raw5, label="Mogadishu")
        plt.plot(itr, Raw6, label="Delhi")
        plt.plot(itr, Raw7, label="Malacca")
        plt.plot(itr, Raw8, label="Nanking")
        plt.plot(itr, Raw9, label="Mexico")
        plt.plot(itr, Raw10, label="Cusco")

        plt.legend(loc=2, ncol=2)

        plt.show()
