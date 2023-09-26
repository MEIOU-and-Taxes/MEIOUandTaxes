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
        
        Total = get_data(t, 'Resident Income Total')
        Innate = get_data(t, 'Resident Income Innate')
        Tax = get_data(t, 'Resident Income Tax')
        Property = get_data(t, 'Resident Income Property')
        Prod = get_data(t, 'Resident Income Prod')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Innate, label="Innate")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        plt.plot(itr, Prod, label="Prod")

        plt.legend(loc=2, ncol=2)

        plt.show()
