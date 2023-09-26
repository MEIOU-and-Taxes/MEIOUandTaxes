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
        
        Salt1 = get_data(t, 'Paris Salt Price')
        Salt2 = get_data(t, 'Moscow Salt Price')
        Salt3 = get_data(t, 'Cairo Salt Price')
        Salt4 = get_data(t, 'Gao Salt Price')
        Salt5 = get_data(t, 'Mogadishu Salt Price')
        Salt6 = get_data(t, 'Delhi Salt Price')
        Salt7 = get_data(t, 'Malacca Salt Price')
        Salt8 = get_data(t, 'Nanking Salt Price')
        Salt9 = get_data(t, 'Mexico Salt Price')
        Salt10 = get_data(t, 'Cusco Salt Price')
        itr = range(1, len(Salt1) + 1)

        plt.plot(itr, Salt1, label="Paris")
        plt.plot(itr, Salt2, label="Moscow")
        plt.plot(itr, Salt3, label="Cairo")
        plt.plot(itr, Salt4, label="Gao")
        plt.plot(itr, Salt5, label="Mogadishu")
        plt.plot(itr, Salt6, label="Delhi")
        plt.plot(itr, Salt7, label="Malacca")
        plt.plot(itr, Salt8, label="Nanking")
        plt.plot(itr, Salt9, label="Mexico")
        plt.plot(itr, Salt10, label="Cusco")

        plt.legend(loc=2, ncol=2)

        plt.show()
