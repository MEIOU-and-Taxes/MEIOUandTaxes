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
        
        food1 = get_data(t, 'Mogadishu Food Price')
        food2 = get_data(t, 'Mogadishu Salt Price')
        food3 = get_data(t, 'Mogadishu Fiber Price')
        food4 = get_data(t, 'Mogadishu Fuel Price')
        food5 = get_data(t, 'Mogadishu Raw Material Price')
        food6 = get_data(t, 'Mogadishu Exotics Price')
        food7 = get_data(t, 'Mogadishu Delicacies Price')
        food8 = get_data(t, 'Mogadishu Naval Product Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Food")
        plt.plot(itr, food2, label="Salt")
        plt.plot(itr, food3, label="Fiber")
        plt.plot(itr, food4, label="Fuel")
        plt.plot(itr, food5, label="Raw")
        plt.plot(itr, food6, label="Exotics")
        plt.plot(itr, food7, label="Delicacies")
        plt.plot(itr, food8, label="Naval")

        plt.legend(loc=2, ncol=2)

        plt.show()
