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
        
        SF = get_data(t, 'Labor SF Fund')
        NM = get_data(t, 'Labor NM Fund')
        RE = get_data(t, 'Labor RE Fund')
        NO = get_data(t, 'Labor NO Fund')
        BG = get_data(t, 'Labor BG Fund')
        CL = get_data(t, 'Labor CL Fund')
        BU = get_data(t, 'Labor BU Fund')
        itr = range(1, len(SF) + 1)

        plt.plot(itr, SF, label="Peasants")
        plt.plot(itr, NM, label="Nomads")
        plt.plot(itr, RE, label="Residents")
        plt.plot(itr, NO, label="Nobles")
        plt.plot(itr, BG, label="Burghers")
        plt.plot(itr, CL, label="Clergy")
        plt.plot(itr, BU, label="State")

        plt.legend(loc=2, ncol=2)

        plt.show()
