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
        
        Fiber1 = get_data(t, 'Paris Fiber Price')
        Fiber2 = get_data(t, 'Moscow Fiber Price')
        Fiber3 = get_data(t, 'Cairo Fiber Price')
        Fiber4 = get_data(t, 'Gao Fiber Price')
        Fiber5 = get_data(t, 'Mogadishu Fiber Price')
        Fiber6 = get_data(t, 'Delhi Fiber Price')
        Fiber7 = get_data(t, 'Malacca Fiber Price')
        Fiber8 = get_data(t, 'Nanking Fiber Price')
        Fiber9 = get_data(t, 'Mexico Fiber Price')
        Fiber10 = get_data(t, 'Cusco Fiber Price')
        itr = range(1, len(Fiber1) + 1)

        plt.plot(itr, Fiber1, label="Paris")
        plt.plot(itr, Fiber2, label="Moscow")
        plt.plot(itr, Fiber3, label="Cairo")
        plt.plot(itr, Fiber4, label="Gao")
        plt.plot(itr, Fiber5, label="Mogadishu")
        plt.plot(itr, Fiber6, label="Delhi")
        plt.plot(itr, Fiber7, label="Malacca")
        plt.plot(itr, Fiber8, label="Nanking")
        plt.plot(itr, Fiber9, label="Mexico")
        plt.plot(itr, Fiber10, label="Cusco")

        plt.legend(loc=2, ncol=2)

        plt.show()
