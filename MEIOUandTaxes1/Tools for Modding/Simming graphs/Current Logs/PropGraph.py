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
        
        Agriculture = get_data(t, 'Building Agriculture Total')
        Forestry = get_data(t, 'Building Forestry Total')
        Extraction = get_data(t, 'Building Extraction Total')
        Fishery = get_data(t, 'Building Fishery Total')
        Industrial = get_data(t, 'Building Industrial Total')
        Commercial = get_data(t, 'Building Commercial Total')
        Academic = get_data(t, 'Building Academic Total')
        Rural = get_data(t, 'Building Rural Total')
        Urban = get_data(t, 'Building Urban Total')
        itr = range(1, len(Urban) + 1)

        plt.plot(itr, Rural, label="Rural", linestyle='--')
        plt.plot(itr, Urban, label="Urban", linestyle='--')
        plt.plot(itr, Agriculture, label="Agriculture")
        plt.plot(itr, Forestry, label="Forestry")
        plt.plot(itr, Extraction, label="Extraction")
        plt.plot(itr, Fishery, label="Fishery")
        plt.plot(itr, Industrial, label="Industrial")
        plt.plot(itr, Commercial, label="Commercial")
        plt.plot(itr, Academic, label="Academic")

        plt.legend(loc=2, ncol=2)

        plt.show()
