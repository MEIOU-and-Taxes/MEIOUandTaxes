from matplotlib import pyplot as plt
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
        
        food = get_data(t, 'Food Production')
        food2 = get_data(t, 'Food DirectBuy')
        fooda = food + food2
        salt = get_data(t, 'Salt Production')
        salt2 = get_data(t, 'Salt DirectBuy')
        salta = salt + salt2
        fiber = get_data(t, 'Fiber Production')
        fiber2 = get_data(t, 'Fiber DirectBuy')
        fibera = fiber + fiber2
        fuel = get_data(t, 'Fuel Production')
        fuel2 = get_data(t, 'Fuel DirectBuy')
        fuela = fuel + fuel2
        raw = get_data(t, 'Raw Material Production')
        delicacies = get_data(t, 'Delicacies Production')
        exotic = get_data(t, 'Exotics Production')
        consumer = get_data(t, 'Consumer Product Production')
        military = get_data(t, 'Military Product Production')
        naval = get_data(t, 'Naval Product Production')
        industrial = get_data(t, 'Industrial Product Production')
        luxury = get_data(t, 'Luxury Product Production')
        knowledge = get_data(t, 'Knowledge Production')
        itr = range(1, len(food) + 1)

        plt.plot(itr, fooda, label="Food")
        plt.plot(itr, salta, label="Salt")
        plt.plot(itr, fibera, label="Fiber")
        plt.plot(itr, fuela, label="Fuel")
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
