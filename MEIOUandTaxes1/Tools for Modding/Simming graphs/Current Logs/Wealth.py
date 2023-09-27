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
        
        wealth = get_data(t, 'Total Wealth')
        wealth2 = get_data(t, 'Infra Wealth')
        itr = range(1, len(wealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, wealth, label="Wealth")
        plt.plot(itr, wealth2, label="Infra Wealth")

        plt.legend(loc=2, ncol=2)

        plt.show()
