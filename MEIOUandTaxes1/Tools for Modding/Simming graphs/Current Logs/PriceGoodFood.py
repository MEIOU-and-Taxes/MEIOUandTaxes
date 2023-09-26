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
        
        food1 = get_data(t, 'Paris Food Price')
        food2 = get_data(t, 'Moscow Food Price')
        food3 = get_data(t, 'Cairo Food Price')
        food4 = get_data(t, 'Gao Food Price')
        food5 = get_data(t, 'Mogadishu Food Price')
        food6 = get_data(t, 'Delhi Food Price')
        food7 = get_data(t, 'Malacca Food Price')
        food8 = get_data(t, 'Nanking Food Price')
        food9 = get_data(t, 'Mexico Food Price')
        food10 = get_data(t, 'Cusco Food Price')
        itr = range(1, len(food1) + 1)

        plt.plot(itr, food1, label="Paris")
        plt.plot(itr, food2, label="Moscow")
        plt.plot(itr, food3, label="Cairo")
        plt.plot(itr, food4, label="Gao")
        plt.plot(itr, food5, label="Mogadishu")
        plt.plot(itr, food6, label="Delhi")
        plt.plot(itr, food7, label="Malacca")
        plt.plot(itr, food8, label="Nanking")
        plt.plot(itr, food9, label="Mexico")
        plt.plot(itr, food10, label="Cusco")

        plt.legend(loc=2, ncol=2)

        plt.show()
