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
        
        Exotics1 = get_data(t, 'Paris Exotics Price')
        Exotics2 = get_data(t, 'Moscow Exotics Price')
        Exotics3 = get_data(t, 'Cairo Exotics Price')
        Exotics4 = get_data(t, 'Gao Exotics Price')
        Exotics5 = get_data(t, 'Mogadishu Exotics Price')
        Exotics6 = get_data(t, 'Delhi Exotics Price')
        Exotics7 = get_data(t, 'Malacca Exotics Price')
        Exotics8 = get_data(t, 'Nanking Exotics Price')
        Exotics9 = get_data(t, 'Mexico Exotics Price')
        Exotics10 = get_data(t, 'Cusco Exotics Price')
        itr = range(1, len(Exotics1) + 1)

        plt.plot(itr, Exotics1, label="Paris")
        plt.plot(itr, Exotics2, label="Moscow")
        plt.plot(itr, Exotics3, label="Cairo")
        plt.plot(itr, Exotics4, label="Gao")
        plt.plot(itr, Exotics5, label="Mogadishu")
        plt.plot(itr, Exotics6, label="Delhi")
        plt.plot(itr, Exotics7, label="Malacca")
        plt.plot(itr, Exotics8, label="Nanking")
        plt.plot(itr, Exotics9, label="Mexico")
        plt.plot(itr, Exotics10, label="Cusco")

        plt.legend(loc=2, ncol=2)

        plt.show()
