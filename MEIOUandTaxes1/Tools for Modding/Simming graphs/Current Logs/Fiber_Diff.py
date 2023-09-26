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
        
        food = get_data(t, 'Europe Fiber R Supply')
        salt = get_data(t, 'ME Fiber R Supply')
        fiber = get_data(t, 'Africa Fiber R Supply')
        fuel = get_data(t, 'India Fiber R Supply')
        raw = get_data(t, 'SEA Fiber R Supply')
        delicacies = get_data(t, 'Asia Fiber R Supply')
        exotic = get_data(t, 'CA Fiber R Supply')
        consumer = get_data(t, 'SA Fiber R Supply')
        military = get_data(t, 'NA Fiber R Supply')
        food2 = get_data(t, 'Europe Fiber R Demand')
        salt2 = get_data(t, 'ME Fiber R Demand')
        fiber2 = get_data(t, 'Africa Fiber R Demand')
        fuel2 = get_data(t, 'India Fiber R Demand')
        raw2 = get_data(t, 'SEA Fiber R Demand')
        delicacies2 = get_data(t, 'Asia Fiber R Demand')
        exotic2 = get_data(t, 'CA Fiber R Demand')
        consumer2 = get_data(t, 'SA Fiber R Demand')
        #military2 = get_data(t, 'NA Fiber R Demand')
        itr = range(1, len(food) + 1)
        food = [food[i]-food2[i] for i in range(len(food))]
        salt = [salt[i]-salt2[i] for i in range(len(salt))]
        fiber = [fiber[i]-fiber2[i] for i in range(len(fiber))]
        fuel = [fuel[i]-fuel2[i] for i in range(len(fuel))]
        raw = [raw[i]-raw2[i] for i in range(len(raw))]
        delicacies = [delicacies[i]-delicacies2[i] for i in range(len(delicacies))]
        exotic = [exotic[i]-exotic2[i] for i in range(len(exotic))]
        consumer = [consumer[i]-consumer2[i] for i in range(len(consumer))]
       # military = [military[i]-military2[i] for i in range(len(military))]

        plt.plot(itr, food, label="Europe")
        plt.plot(itr, salt, label="Middle East")
        plt.plot(itr, fiber, label="Africa")
        plt.plot(itr, fuel, label="India")
        plt.plot(itr, raw, label="Southeast Asia")
        plt.plot(itr, delicacies, label="Asia + Japan")
        plt.plot(itr, exotic, label="Central Asia")
        plt.plot(itr, consumer, label="South America")
        #plt.plot(itr, military, label="North America")

        plt.legend(loc=2, ncol=2)

        plt.show()
