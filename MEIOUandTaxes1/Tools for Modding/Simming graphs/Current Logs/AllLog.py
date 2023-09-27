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
        
        food = get_data(t, 'Global Food Price')
        salt = get_data(t, 'Global Salt Price')
        fiber = get_data(t, 'Global Fiber Price')
        fuel = get_data(t, 'Global Fuel Price')
        raw = get_data(t, 'Global Raw Material Price')
        delicacies = get_data(t, 'Global Delicacies Price')
        exotic = get_data(t, 'Global Exotics Price')
        consumer = get_data(t, 'Global Consumer Product Price')
        military = get_data(t, 'Global Military Product Price')
        naval = get_data(t, 'Global Naval Product Price')
        industrial = get_data(t, 'Global Industrial Product Price')
        luxury = get_data(t, 'Global Luxury Product Price')
        knowledge = get_data(t, 'Global Knowledge Price')
        itr = range(1, len(food) + 1)

        plt.plot(itr, food, 'tab:blue', label="Food")
        plt.plot(itr, salt, 'tab:orange', label="Salt")
        plt.plot(itr, fiber, 'tab:green', label="Fiber")
        plt.plot(itr, fuel, 'tab:red', label="Fuel")
        plt.plot(itr, raw, 'tab:purple', label="Raw")
        plt.plot(itr, delicacies, label="Delicacies")
        plt.plot(itr, exotic, 'tab:brown', label="Exotic")
        plt.plot(itr, consumer, 'tab:pink', label="Consumer")
        plt.plot(itr, military, 'tab:gray', label="Military")
        plt.plot(itr, naval, 'tab:olive', label="Naval")
        plt.plot(itr, industrial, 'tab:cyan', label="Industrial")
        plt.plot(itr, luxury, 'rosybrown', label="Luxury")
        plt.plot(itr, knowledge, 'teal', label="Knowledge")
        
        plt.yscale('log')

        plt.legend(loc=2, ncol=2)

        plt.show()
