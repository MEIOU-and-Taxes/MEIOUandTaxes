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

if __name__ == '__main__':
    with open('game.log') as f:
        t = f.read()
        
        food = get_data(t, 'Europe Food R Supply')
        salt = get_data(t, 'ME Food R Supply')
        fiber = get_data(t, 'Africa Food R Supply')
        fuel = get_data(t, 'India Food R Supply')
        raw = get_data(t, 'SEA Food R Supply')
        delicacies = get_data(t, 'Asia Food R Supply')
        exotic = get_data(t, 'CA Food R Supply')
        consumer = get_data(t, 'SA Food R Supply')
        military = get_data(t, 'NA Food R Supply')
        food2 = get_data(t, 'Europe Food R Demand')
        salt2 = get_data(t, 'ME Food R Demand')
        fiber2 = get_data(t, 'Africa Food R Demand')
        fuel2 = get_data(t, 'India Food R Demand')
        raw2 = get_data(t, 'SEA Food R Demand')
        delicacies2 = get_data(t, 'Asia Food R Demand')
        exotic2 = get_data(t, 'CA Food R Demand')
        consumer2 = get_data(t, 'SA Food R Demand')
        military2 = get_data(t, 'NA Food R Demand')
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

        plt.plot(itr, food, label="Europe")
        plt.plot(itr, salt, label="Middle East")
        plt.plot(itr, fiber, label="Africa")
        plt.plot(itr, fuel, label="India")
        plt.plot(itr, raw, label="Southeast Asia")
        plt.plot(itr, delicacies, label="Asia + Japan")
        plt.plot(itr, exotic, label="Central Asia")
        plt.plot(itr, consumer, label="South America")
        plt.plot(itr, military, label="North America")

        plt.legend(loc=2, ncol=2)

        plt.show()
