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
        
        wealth = get_data(t, 'Infra Wealth')
        itr = range(1, len(wealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, wealth, label="Wealth")

        plt.legend(loc=2, ncol=2)

        plt.show()
