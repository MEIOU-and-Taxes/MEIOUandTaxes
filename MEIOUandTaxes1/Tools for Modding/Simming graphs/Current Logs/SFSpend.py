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
        
        Total = get_data(t, 'Peasant Spend Total')
        Tax = get_data(t, 'Peasant Spend Tax')
        Property = get_data(t, 'Peasant Spend Property')
        #Infra = get_data(t, 'Peasant Spend Infra')
        Prod = get_data(t, 'Peasant Spend Prod')
        itr = range(1, len(Total) + 1)

        plt.plot(itr, Total, label="Total")
        plt.plot(itr, Tax, label="Tax")
        plt.plot(itr, Property, label="Property")
        #plt.plot(itr, Infra, label="Infra")
        plt.plot(itr, Prod, label="Prod")

        plt.legend(loc=2, ncol=2)

        plt.show()
