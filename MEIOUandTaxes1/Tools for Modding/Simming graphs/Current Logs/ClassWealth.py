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
        
        sfwealth = get_data(t, 'Peasant Wealth')
        nmwealth = get_data(t, 'Nomad Wealth')
        rewealth = get_data(t, 'Resident Wealth')
        nowealth = get_data(t, 'Noble Wealth')
        bgwealth = get_data(t, 'Burgher Wealth')
        clwealth = get_data(t, 'Clergy Wealth')
        itr = range(1, len(sfwealth) + 1)

        #plt.plot(itr, wage, label="Total")
        plt.plot(itr, sfwealth, label="Peasant")
        plt.plot(itr, nmwealth, label="Nomad")
        plt.plot(itr, rewealth, label="Resident")
        plt.plot(itr, nowealth, label="Noble")
        plt.plot(itr, bgwealth, label="Burgher")
        plt.plot(itr, clwealth, label="Clergy")

        plt.legend(loc=2, ncol=2)

        plt.show()
