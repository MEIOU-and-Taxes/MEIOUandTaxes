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
        
        Innate = get_data(t, 'Genoa commercial size')
        Gold = get_data(t, 'Venice commercial size')
        itr = range(1, len(Innate) + 1)

        plt.plot(itr, Innate, label="Genoa")
        plt.plot(itr, Gold, label="Venice")

        plt.legend(loc=2, ncol=2)

        plt.show()
