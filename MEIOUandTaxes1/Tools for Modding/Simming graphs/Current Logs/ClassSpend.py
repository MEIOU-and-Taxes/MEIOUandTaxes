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
        
        sfwealth = get_data(t, 'Peasant Spend Total')
        nmwealth = get_data(t, 'Nomad Spend Total')
        rewealth = get_data(t, 'Resident Spend Total')
        nowealth = get_data(t, 'Noble Spend Total')
        bgwealth = get_data(t, 'Burgher Spend Total')
        clwealth = get_data(t, 'Clergy Spend Total')
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
