from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd

def get_data(t, i):
    lst = []
    loc = 0

    while True:
        loc = t.find(i, loc)

        if loc != -1:
            end = t.find('\n', loc)
            lst.append(float(t[loc:end].strip().split(':')[1].strip().split("£")[-1]))
            loc = end
        else:
            break

    return lst

def to_percent(y, position):
    return f"{round(y * 100, 3)}%"

if __name__ == '__main__':
    with open('game.log') as f:
        t = f.read()
        


        formatter = FuncFormatter(to_percent)

        #SF = get_data(t, 'Peasant Pop Total')
        #NM = get_data(t, 'Nomads Pop Total')
        #RE = get_data(t, 'Residents Pop Total')
        NO = get_data(t, 'Nobles Pop Total')
        BG = get_data(t, 'Burghers Pop Total')
        CL = get_data(t, 'Clergy Pop Total')


        #SF_gr = result = [y / x - 1 for x, y in zip(SF[:-1], SF[1:])]
        #NM_gr = result = [y / x - 1 for x, y in zip(NM[:-1], NM[1:])]
        #RE_gr = result = [y / x - 1 for x, y in zip(RE[:-1], RE[1:])]
        NO_gr = result = [y / x - 1 for x, y in zip(NO[:-1], NO[1:])]
        BG_gr = result = [y / x - 1 for x, y in zip(BG[:-1], BG[1:])]
        CL_gr = result = [y / x - 1 for x, y in zip(CL[:-1], CL[1:])]


        itr = range(1, len(NO_gr) + 1)

        plt.title("Elites - Growth Rate per Class against YoY")
        #plt.plot(itr, SF_gr, label="Peasants")
        #plt.plot(itr, NM_gr, label="Nomads")
        #plt.plot(itr, RE_gr, label="Residents")
        plt.plot(itr, NO_gr, label="Nobles")
        plt.plot(itr, BG_gr, label="Burghers")
        plt.plot(itr, CL_gr, label="Clergy")
        plt.gca().yaxis.set_major_formatter(formatter)

        plt.legend(loc=2, ncol=2)

        plt.show()
