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

if __name__ == '__main__':
    with open('game.log') as f:
        t = f.read()
        
        food = get_data(t, 'Food Demand')
        salt = get_data(t, 'Salt Demand')
        fiber = get_data(t, 'Fiber Demand')
        fuel = get_data(t, 'Fuel Demand')
        raw = get_data(t, 'Raw Material Demand')
        delicacies = get_data(t, 'Delicacies Demand')
        exotic = get_data(t, 'Exotics Demand')
        consumer = get_data(t, 'Consumer Product Demand')
        military = get_data(t, 'Military Product Demand')
        naval = get_data(t, 'Naval Product Demand')
        industrial = get_data(t, 'Industrial Product Demand')
        luxury = get_data(t, 'Luxury Product Demand')
        knowledge = get_data(t, 'Knowledge Demand')
        itr = range(1, len(food) + 1)

        #plt.plot(itr, food, label="Food")
        plt.plot(itr, salt, label="Salt")
        plt.plot(itr, fiber, label="Fiber")
        plt.plot(itr, fuel, label="Fuel")
        plt.plot(itr, raw, label="Raw")
        plt.plot(itr, delicacies, label="Delicacies")
        plt.plot(itr, exotic, label="Exotic")
        plt.plot(itr, consumer, label="Consumer")
        plt.plot(itr, military, label="Military")
        plt.plot(itr, naval, label="Naval")
        plt.plot(itr, industrial, label="Industrial")
        plt.plot(itr, luxury, label="Luxury")
        plt.plot(itr, knowledge, label="Knowledge")

        plt.legend(loc=2, ncol=2)

        plt.show()
