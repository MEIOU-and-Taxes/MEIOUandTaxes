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

    return lst

if __name__ == '__main__':
    with open('game.log') as f:
        t = f.read()
        
        foodp = np.array(get_data(t, 'Europe Food R Supply'))
        foodd = np.array(get_data(t, 'Europe Food R Demand'))
        foode = np.array(get_data(t, 'Europe Food R Direct'))
        foodf = foodd + foode
        foodj = foodp + foode
        itr = range(1, len(foodp) + 1)

        plt.plot(itr, foodp, label="Production")
        plt.plot(itr, foodd, label="Market Demand")
        plt.plot(itr, foode, label="Direct Buy")
        plt.plot(itr, foodf, label="Total Demand")
        plt.plot(itr, foodj, label="Total Production")

        plt.legend(loc=2, ncol=2)

        plt.show()
