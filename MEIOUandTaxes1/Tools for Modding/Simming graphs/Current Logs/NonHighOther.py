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
        
        pwealth = get_data(t, 'Peasant Wealth')
        nwealth = get_data(t, 'Nomad Wealth')
        rwealth = get_data(t, 'Resident Wealth')
        nowealth = get_data(t, 'Noble Wealth')
        bwealth = get_data(t, 'Burgher Wealth')
        cwealth = get_data(t, 'Clergy Wealth')
        #wealth = get_data(t, 'Wealth')
        itr = range(1, len(pwealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, pwealth, label="Peasants")
        plt.plot(itr, nwealth, label="Nomads")
        plt.plot(itr, rwealth, label="Residents")
        plt.plot(itr, nowealth, label="Nobles")
        plt.plot(itr, bwealth, label="Burghers")
        plt.plot(itr, cwealth, label="Clergy")
        #plt.plot(itr, wealth, label="Wealth")

        plt.legend(loc=2, ncol=2)

        plt.show()
