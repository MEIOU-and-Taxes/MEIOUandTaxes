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
        
        Naval1 = get_data(t, 'Paris Naval Product Price')
        Naval2 = get_data(t, 'Moscow Naval Product Price')
        Naval3 = get_data(t, 'Cairo Naval Product Price')
        Naval4 = get_data(t, 'Gao Naval Product Price')
        Naval5 = get_data(t, 'Mogadishu Naval Product Price')
        Naval6 = get_data(t, 'Delhi Naval Product Price')
        Naval7 = get_data(t, 'Malacca Naval Product Price')
        Naval8 = get_data(t, 'Nanking Naval Product Price')
        Naval9 = get_data(t, 'Mexico Naval Product Price')
        Naval10 = get_data(t, 'Cusco Naval Product Price')
        itr = range(1, len(Naval1) + 1)

        plt.plot(itr, Naval1, label="Paris")
        plt.plot(itr, Naval2, label="Moscow")
        plt.plot(itr, Naval3, label="Cairo")
        plt.plot(itr, Naval4, label="Gao")
        plt.plot(itr, Naval5, label="Mogadishu")
        plt.plot(itr, Naval6, label="Delhi")
        plt.plot(itr, Naval7, label="Malacca")
        plt.plot(itr, Naval8, label="Nanking")
        plt.plot(itr, Naval9, label="Mexico")
        plt.plot(itr, Naval10, label="Cusco")

        plt.legend(loc=2, ncol=2)

        plt.show()
