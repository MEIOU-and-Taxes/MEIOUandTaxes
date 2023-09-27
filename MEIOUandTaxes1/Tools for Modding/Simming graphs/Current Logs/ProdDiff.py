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

    return np.array(lst)

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
        
        food = get_data(t, 'Food Production')
        salt = get_data(t, 'Salt Production')
        fiber = get_data(t, 'Fiber Production')
        fuel = get_data(t, 'Fuel Production')
        raw = get_data(t, 'Raw Material Production')
        delicacies = get_data(t, 'Delicacies Production')
        exotic = get_data(t, 'Exotics Production')
        consumer = get_data(t, 'Consumer Product Production')
        military = get_data(t, 'Military Product Production')
        naval = get_data(t, 'Naval Product Production')
        industrial = get_data(t, 'Industrial Product Production')
        luxury = get_data(t, 'Luxury Product Production')
        knowledge = get_data(t, 'Knowledge Production')
        food2 = get_data(t, 'Food Demand')
        salt2 = get_data(t, 'Salt Demand')
        fiber2 = get_data(t, 'Fiber Demand')
        fuel2 = get_data(t, 'Fuel Demand')
        raw2 = get_data(t, 'Raw Material Demand')
        delicacies2 = get_data(t, 'Delicacies Demand')
        exotic2 = get_data(t, 'Exotics Demand')
        consumer2 = get_data(t, 'Consumer Product Demand')
        military2 = get_data(t, 'Military Product Demand')
        naval2 = get_data(t, 'Naval Product Demand')
        industrial2 = get_data(t, 'Industrial Product Demand')
        luxury2 = get_data(t, 'Luxury Product Demand')
        knowledge2 = get_data(t, 'Knowledge Demand')
        food3 = get_data(t, 'Food DirectBuy')
        salt3 = get_data(t, 'Salt DirectBuy')
        fiber3 = get_data(t, 'Fiber DirectBuy')
        fuel3 = get_data(t, 'Fuel DirectBuy')
        food = food + food3
        salt = salt + salt3
        fiber = fiber + fiber3
        fuel = fuel + fuel3
        food2 = food2 + food3
        salt2 = salt2 + salt3
        fiber2 = fiber2 + fiber3
        fuel2 = fuel2 + fuel3
        itr = range(1, len(food) + 1)
        food = [food[i]-food2[i] for i in range(len(food))]
        salt = [salt[i]-salt2[i] for i in range(len(salt))]
        fiber = [fiber[i]-fiber2[i] for i in range(len(fiber))]
        fuel = [fuel[i]-fuel2[i] for i in range(len(fuel))]
        raw = [raw[i]-raw2[i] for i in range(len(raw))]
        delicacies = [delicacies[i]-delicacies2[i] for i in range(len(delicacies))]
        exotic = [exotic[i]-exotic2[i] for i in range(len(exotic))]
        consumer = [consumer[i]-consumer2[i] for i in range(len(consumer))]
        military = [military[i]-military2[i] for i in range(len(military))]
        naval = [naval[i]-naval2[i] for i in range(len(naval))]
        industrial = [industrial[i]-industrial2[i] for i in range(len(industrial))]
        luxury = [luxury[i]-luxury2[i] for i in range(len(luxury))]
        knowledge = [knowledge[i]-knowledge2[i] for i in range(len(knowledge))]

        plt.plot(itr, food, label="Food")
        plt.plot(itr, salt, label="Salt")
        plt.plot(itr, fiber, label="Fiber")
        plt.plot(itr, fuel, label="Fuel")
        plt.plot(itr, raw, label="Raw")
        plt.plot(itr, delicacies, label="Delicacies")
        plt.plot(itr, exotic, label="Exotics")
        plt.plot(itr, consumer, label="Consumer")
        plt.plot(itr, military, label="Military")
        plt.plot(itr, naval, label="Naval")
        plt.plot(itr, industrial, label="Industrial")
        plt.plot(itr, luxury, label="Luxury")
        plt.plot(itr, knowledge, label="Knowledge")

        plt.legend(loc=2, ncol=2)

        plt.show()
