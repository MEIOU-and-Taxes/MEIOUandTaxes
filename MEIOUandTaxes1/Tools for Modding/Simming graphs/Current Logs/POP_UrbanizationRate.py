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

        SF = get_data(t, 'Peasant Pop Total')
        NM = get_data(t, 'Nomads Pop Total')
        RE = get_data(t, 'Residents Pop Total')


        lower_classes = [a + b for a, b in zip(NM, SF)]
        urbanization = [a / b for a, b in zip(RE, lower_classes)]

        itr = range(1, len(urbanization) + 1)

        plt.title("Global Urbanization Rate")
        plt.plot(itr, urbanization, label="Urbanization Rate - RE/(SF+NM)")
        plt.gca().yaxis.set_major_formatter(formatter)

        plt.legend(loc=2, ncol=2)

        plt.show()
